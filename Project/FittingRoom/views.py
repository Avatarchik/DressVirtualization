from django.shortcuts import render
from django.http import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib import messages
from django.conf import settings
import os
import json
import logging
# import boto3
# from botocore.exceptions import ClientError
import cv2
import imutils


def home(request):
    sample_dresses_path_list, uploaded_dresses_path_list = {}, {}
    sample_dresses_midpoint, uploaded_dresses_midpoint = {}, {}

    if request.user.is_authenticated:
        user_name = str(request.user.username)
        path_to_sample_dresses = 'FittingRoom/Dresses/'
        path_to_uploaded_dresses = 'FittingRoom/static/FittingRoom/upload/users/' + request.user.username
        full_path_to_sample_dresses = os.path.join(settings.STATIC_ROOT, path_to_sample_dresses)

        print(f'\nPath to {user_name} exist: {os.path.exists(path_to_uploaded_dresses)}\n')

        # check_bucket_exist(user_name)
        # if not request.user.is_superuser:
        #     get_all_s3_keys(user_name)

        count = 0
        for filename in os.listdir(full_path_to_sample_dresses):
            key = 'sample_dress' + str(count)
            value = '/static/' + path_to_sample_dresses + filename
            mid = find_middle(value)

            sample_dresses_path_list[key] = value
            sample_dresses_midpoint[key] = mid

            count += 1

        if os.path.exists(path_to_uploaded_dresses):
            count = 0
            path_to_uploaded_dresses += '/dresses/'

            check_valid_dresses(request)

            for filename in os.listdir(path_to_uploaded_dresses):
                key = 'uploaded_dress' + str(count)
                value = '/static/FittingRoom/upload/users/' + user_name + '/dresses/' + filename
                mid = find_middle(value)

                uploaded_dresses_path_list[key] = value
                uploaded_dresses_midpoint[key] = mid

                count += 1
        else:
            print(f'\nUser \"{user_name}\" has not imported any dresses\n')

        print(f'\nSample Dress List:\n{sample_dresses_path_list}\n')
        print(f'\nSample Dress Midpoint List:\n{sample_dresses_midpoint}\n')
        print(f'\nUploaded Dress List:\n{uploaded_dresses_path_list}\n')
        print(f'\nUploaded Dress Midpoint List:\n{uploaded_dresses_midpoint}\n')

    context = {
        'title': 'Home',
        'sample_dresses_path_list': sample_dresses_path_list,
        'uploaded_dresses_path_list': uploaded_dresses_path_list,
        'js_sample_dresses_data': json.dumps(sample_dresses_path_list),
        'js_uploaded_dresses_data': json.dumps(uploaded_dresses_path_list),
        'js_sample_dresses_midpoint_data': json.dumps(sample_dresses_midpoint),
        'js_uploaded_dresses_midpoint_data': json.dumps(uploaded_dresses_midpoint)
    }

    if request.user.is_authenticated:
        return render(request, 'FittingRoom/home.html', context)
    else:
        return render(request, 'FittingRoom/default_home.html', { 'title': 'Home' })


def find_middle(file_name):
    file_name = 'FittingRoom/' + file_name
    # Load the image, convert to grayscale and blur slightly
    image = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # Find contours in the threshold image
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    middle = 0

    # Loop over the contours
    for each in contours:
        # compute the center of the contour
        M = cv2.moments(each)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        middle = cX
    return middle


def check_valid_dresses(request):
    path = settings.UPLOAD_ROOT + '/users/' + request.user.username + '/dresses/'
    for filename in os.listdir(path):
        file_name = path + filename

        img = cv2.pyrDown(cv2.imread(file_name, cv2.IMREAD_UNCHANGED))
        ret, threshed_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 127, 255, cv2.THRESH_BINARY)
        contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        x_list, y_list = [], []
        for each in contours:
            x, y, w, h = cv2.boundingRect(each)
            x_list.append(x)
            y_list.append(y)

        rect_x, rect_y = min(x_list), min(y_list)
        rect_w, rect_h = 0, 0
        found_contour = False

        for each in contours:
            x, y, w, h = cv2.boundingRect(each)

            if x == rect_x and y == rect_y:
                found_contour = True

        if not found_contour:
            print(f'Contour for \"{filename}\" not found.')
            delete_imported_dress(request, file_name, path)

def delete_imported_dress(request, file_name, path):
    img_to_delete = file_name
    img = os.path.basename(img_to_delete)
    print(f'img: {img}')

    for filename in os.listdir(path):
        print(f'filename: {filename}')
        if filename == img:
            os.remove(img_to_delete)
            print(f'\nFile has been deleted.')


# def check_bucket_exist(user_name):
#     bucket_name = user_name + '-files'
#     print(f'This is the bucket name: {bucket_name}')
#     s3 = boto3.resource('s3')
#     if s3.Bucket(bucket_name).creation_date is None:
#         print(f'Date of bucket is None')
#         create_bucket(bucket_name)
#     else:
#         print(f'Bucket \"{bucket_name}\" exists.')
#
#
# def create_bucket(bucket_name):
#     try:
#         s3_client = boto3.client('s3')
#         s3_client.create_bucket(Bucket = bucket_name)
#         print(f'Bucket \"{bucket_name}\" has been created!')
#     except ClientError as e:
#         logging.error(e)
#         return False
#     return True
#
#
# def get_all_s3_keys(user_name):
#     '''Get a list of all keys in an S3 bucket.'''
#     bucket_name = user_name + '-files'
#     s3 = boto3.client('s3')
#     resp = s3.list_objects_v2(Bucket = bucket_name)
#
#     if resp['KeyCount'] != 0:
#         keys = []
#         kwargs = { 'Bucket': bucket_name }
#         for obj in resp['Contents']:
#             keys.append(obj['Key'])


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
