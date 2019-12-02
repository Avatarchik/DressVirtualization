from django.shortcuts import render
from django.http import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.conf import settings
import os
import json


def home(request):
    sample_files_list, upload_files_list = [], []
    upload_dress_list, upload_dress_path_list = {}, {}
    sample_dress_list, sample_dress_path_list = {}, {}

    path_to_sample_dress = "FittingRoom/Dresses/"

    for filename in os.listdir(os.path.join(settings.STATIC_ROOT, path_to_sample_dress)):
        sample_files_list.append(filename)
        print(f"\n\nThis File_name: {filename}\n\n")

    sample_files_list_length = len(sample_files_list)
    for idx in range(sample_files_list_length):
        sample_dress_key = 'sample_dress' + str(idx)
        sample_dress_value = sample_files_list[idx]
        sample_path_value = "/static/" + path_to_sample_dress + sample_files_list[idx]

        sample_dress_list[sample_dress_key] = sample_dress_value
        sample_dress_path_list[sample_dress_key] = sample_path_value

    if request.user.is_authenticated:
        path_to_upload_dress = 'FittingRoom/static/FittingRoom/upload/users/' + request.user.username

        print(f'\n\nPath exist?  {os.path.exists(path_to_upload_dress)}\n\n')
        if os.path.exists(path_to_upload_dress):
            for filename in os.listdir(path_to_upload_dress + "/dresses/"):
                upload_files_list.append(filename)

            print(f'\n\nupload_files_list: {upload_files_list}\n\n')

            upload_files_list_length = len(upload_files_list)
            for idx in range(upload_files_list_length):
                upload_dress_key = 'upload_dress' + str(idx)
                upload_dress_value = upload_files_list[idx]
                upload_path_value = '/static/FittingRoom/upload/users/' + request.user.username + '/dresses/' + upload_files_list[idx]

                upload_dress_list[upload_dress_key] = upload_dress_value
                upload_dress_path_list[upload_dress_key] = upload_path_value
        else:
                print(f'\n\nUser {request.user.username} has not imported any dresses\n\n')

    js_sample_dress_data = sample_dress_path_list
    js_upload_dress_data = upload_dress_path_list

    context = {
        "title": "Home",
        "sample_dress_list": sample_dress_list,
        "sample_dress_path_list": sample_dress_path_list,
        "upload_dress_list": upload_dress_list,
        "upload_dress_path_list": upload_dress_path_list,
        "js_sample_dress_data": json.dumps(js_sample_dress_data),
        "js_upload_dress_data": json.dumps(js_upload_dress_data)
    }

    print(f'\n\nsample_dress_list: {sample_dress_list}\n')
    print(f'sample_dress_path_list: {sample_dress_path_list}\n')
    print(f'upload_dress_list: {upload_dress_list}\n')
    print(f'upload_dress_path_list: {upload_dress_path_list}\n')

    if request.user.is_authenticated:
        return render(request, 'FittingRoom/home.html', context)
    else:
        return render(request, 'FittingRoom/default_home.html', { 'title': 'Home' })


def display_model(request):
    return render(request, 'FittingRoom/model.html', { 'title': 'Our Model' })


def contact(request):
    return render(request, 'FittingRoom/contact.html', { 'title': 'Contact' })


@csrf_exempt
def dress_library(request):
    files_list, dress_list = [], {}
    for filename in os.listdir(os.path.join(settings.STATIC_ROOT, 'FittingRoom/Dresses/')):
        files_list.append(filename)

    for idx in range(len(files_list)):
        key, value = 'dress' + str(idx), files_list[idx]
        dress_list[key] = value

    context = {
        'dress_list': dress_list
    }

    print(f'files_list: {files_list}')
    print(f'context: {dress_list}')
    return render(request, 'FittingRoom/homeDress.html', context, {'title': 'Test'})
