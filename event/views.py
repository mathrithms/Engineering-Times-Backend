from django.shortcuts import render, redirect


def main_view(request):
    return render(request, 'admin/crop_image.html')
