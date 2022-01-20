import base64
import time

import cv2
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .detect_mask_image import mask_image
from .detect_mask_video import start_video
from .forms import PhotoForm
from .models import Photo
from .train_mask_detector import train_model


class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():

            photo = form.save()
            data = {'is_valid': True, 'name': photo.name}
            try:
                with open('mask_detector.model'):
                    data['status'] = True
                    frame = mask_image(photo.path.url)
                    ret, frame_buff = cv2.imencode('.jpg', frame)  # could be png, update html as well
                    frame_b64 = base64.b64encode(frame_buff)
                    data['image'] = frame_b64.decode()
                    print(data)
            except Exception:
                data['status'] = False


        else:
            data = {'is_valid': False}
        return JsonResponse(data, safe=True)


class startTraining(View):
    def get(self, request):

        data = {}

        train_model()
        with open('plot.png', 'rb') as f:
            img = f.read()
            frame_b64 = base64.b64encode(img)
            data['image'] = frame_b64.decode()
        return JsonResponse(data, safe=True)


class checkTraining(View):
    def get(self, request):
        data = {}
        try:
            with open('mask_detector.model'):
                data['status'] = True
        except Exception:
            data['status'] = False
        return JsonResponse(data, safe=True)

class startVideo(View):
    def get(self, request):
        start_video()
        return JsonResponse('', safe=True)


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(
            1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))
