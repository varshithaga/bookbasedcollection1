import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import UploadedFile, Frame
from PyPDF2 import PdfReader
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

def generate_prompt(text_chunk):
    first_sentence = text_chunk.split('.')[0]
    return f"Illustrate this scene: {first_sentence.strip()}."

def home(request):
    return render(request, 'pdfsplitter/home.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def split_text(text, n):
    sentences = re.split(r'(?<=[.!?]) +', text)
    total = len(sentences)
    chunk_size = total // n
    chunks = []
    for i in range(n):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < n - 1 else total
        chunk = " ".join(sentences[start:end])
        chunks.append(chunk)
    return chunks

@login_required
def view_frames(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id, user=request.user)
    frames = uploaded_file.frames.all()
    print(uploaded_file,"ooo")
    print(frames,"ooo778788")
    return render(request, 'pdfsplitter/frames.html', {'frames': frames, 'file': uploaded_file})


@csrf_exempt
@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()

            return redirect('enter_frames', file_id=uploaded_file.id)
    else:
        form = UploadFileForm()
    return render(request, 'pdfsplitter/upload.html', {'form': form})


@login_required
def enter_frames(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id, user=request.user)

    if request.method == 'POST':
        n_frames = int(request.POST.get('n_frames', 5))
        return redirect('generate_frames', file_id=file_id, n_frames=n_frames)

    return render(request, 'pdfsplitter/enter_frames.html', {'file': uploaded_file})

@login_required
def generate_frames(request, file_id, n_frames):
    import os
    import requests
    from PIL import Image
    from io import BytesIO
    from django.core.files.base import ContentFile

    # Get uploaded file object
    uploaded_file = UploadedFile.objects.get(id=file_id, user=request.user)
    file_path = uploaded_file.file.path
    text = ""

    # Read text
    if uploaded_file.file.name.endswith('.pdf'):
        from PyPDF2 import PdfReader
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    elif uploaded_file.file.name.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        return redirect('upload_pdf')

    # Split text and generate prompts
    chunks = split_text(text, n_frames)
    prompts = [generate_prompt(chunk) for chunk in chunks]

    from dotenv import load_dotenv
    load_dotenv()

    HF_TOKEN = os.getenv("HF_TOKEN")


    # Image generation function
    # HF_TOKEN = os.environ.get("HF_TOKEN")
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}

    def generate_image(prompt):
        payload = {"inputs": prompt}
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.headers.get("content-type", "").startswith("application/json"):
            error_data = response.json()
            print(f"Error generating image for prompt:\n'{prompt}'")
            print("Error message:", error_data)
            return None

        try:
            image = Image.open(BytesIO(response.content))
            return image
        except Exception as e:
            print(f"Failed to open image for prompt:\n'{prompt}'")
            print("Exception:", e)
            return None

    # Generate and save frames to the DB
    from .models import Frame  # Import your Frame model

    for i, prompt in enumerate(prompts, 1):
        print(f"\nGenerating image for Frame {i}: {prompt}")
        img = generate_image(prompt)
        if img:
            # Convert to in-memory file
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_content = ContentFile(img_io.getvalue(), f"frame_{i}.png")

            # Save Frame instance
            frame = Frame.objects.create(
                uploaded_file=uploaded_file,
                prompt=prompt,
                frame_number=i,
                generated_image=img_content
            )
            print(f"Saved Frame {i} to database with ID")
        else:
            print(f"Skipping Frame {i} due to error.")

    print("\n===== All frames processed and saved to database =====")

    # Redirect to view the frames (or render a template directly!)
    return redirect('view_frames', file_id=uploaded_file.id)
 