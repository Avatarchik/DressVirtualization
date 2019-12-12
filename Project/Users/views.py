from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
import cv2
import imutils
import numpy as np
from PIL import Image
import os
import logging
# import boto3
# from botocore.exceptions import ClientError


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created! for {username}\
            Please log in with you new username and password')
            return redirect('User-Login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})


@login_required     # Add functionality to an existing function
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Account successfully updated')
            return redirect('User-Profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'title': "Profile",
        'user_form': u_form,
        'profile_form': p_form
     }

    from django.http import HttpResponse as response
    response('<h1>{{}}</h1>')
    print(f'\n\nContext: {context}\n\n')
    return render(request, 'Users/profile.html', context)


@login_required
def adminLogout(request):
    return redirect('FittingRoom-Home')


@login_required
def upload_dress(request):
    context = {  }
    if request.method == 'POST':
        dress = request.FILES['dress_image']

        save_file_url = settings.UPLOAD_ROOT + '/users/' + request.user.username + '/dresses/'

        dress_path = save_file_url + dress.name
        upload_storage = FileSystemStorage(location = save_file_url, base_url = settings.UPLOAD_ROOT)
        name = upload_storage.save(dress.name, dress)

        context['url'] = upload_storage.url(name)

        new_file_name = remove_black_background(dress_path, save_file_url)
        resize_upload(request, new_file_name)

        # if not request.user.is_superuser:
        #     upload_to_s3(request, new_file_name)

    return render(request, 'Users/upload.html')


def admin_upload(request):
    context = {  }
    if request.method == 'POST':
        dress = request.FILES['dress_image']

        save_file_url = settings.STATIC_ROOT + '/FittingRoom/Dresses/'

        dress_path = save_file_url + dress.name
        upload_storage = FileSystemStorage(location = save_file_url, base_url = settings.STATIC_ROOT)
        name = upload_storage.save(dress.name, dress)

        context['url'] = upload_storage.url(name)

        new_file_name = remove_black_background(dress_path, save_file_url)
        resize_upload(request, new_file_name)

    return render(request, 'Users/adminUpload.html')


# def upload_to_s3(request, file_name, bucket_name = None, object_name = None):
#     bucket_name = str(request.user.username) + '-files'
#
#     # If S3 object_name was not specified, then use new_file_name
#     if object_name is None:
#         object_name = file_name
#
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(str(file_name), bucket_name, object_name)
#         # print(f'File \"{file_name}\" was successfully uploaded to AWS S3!')
#     except ClientError as e:
#         logging.error(e)
#         return False
#
#     return True


def show(name, img):
    cv2.imshow(name, img)
    while True:
        key = cv2.waitKey(1)
        if key == 27: break


def resize_upload(request, dress_file):
    file_name = dress_file

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
            rect_w, rect_h = w, h
            found_contour = True

            # print(f"\n\nrect_x: {rect_x}\n")
            # print(f"rect_y: {rect_y}\n")
            # print(f"rect_w: {rect_w}\n")
            # print(f"rect_h: {rect_h}\n")
            # print(f"(x, y): ({rect_x}, {rect_y})\n")
            # print(f"(x+w, y+h): ({rect_x + rect_w}, {rect_y + rect_h})\n")

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            break

    if found_contour:
        img_height, img_width = img.shape[:2]

        # print(f"\n\nImg Dimension: {img.shape[:2]}\n\n")
        # show("img", img)

        try:
            img1 = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
            # print(f"\n\nimg1 dimension: {img1.shape[:2]}\n\n")
            # show("img1", img1)

            try:
                resized = cv2.resize(img1, (img_width, img_height), interpolation = cv2.INTER_AREA)
                # show("resized", resized)
                cv2.imwrite(file_name, resized)

                try:
                    img_crop = Image.open(file_name)
                    width, height = img_crop.size
                    # print(f"\n\nimg_crop: ({width}, {height})\n\n")
                    result = img_crop.crop((rect_x, rect_y, (rect_x + rect_w), (rect_y + rect_h)))
                    result.save(file_name, "PNG")
                except:
                    # print(f"\n\nCropping to ({rect_x}, {rect_y}, ({rect_x + rect_w}), ({rect_y + rect_h})) error\n\n")
                    pass
            except:
                # print(f"\n\nResize to ({img_width}, {img_height}) error\n\n")
                pass
        except:
            # print("\n\nReading Img1 error\n\n")
            pass

        # while True:
        #     key = cv2.waitKey(1)
        #     if key == 27: break
        # cv2.destroyAllWindows()

        try:
            rescaled = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
            resize_resized = cv2.resize(rescaled, (900, 827), interpolation = cv2.INTER_AREA)
            cv2.imwrite(file_name, resize_resized)
        except:
            # print("\n\nResize to (900, 827) error\n\n")
            pass
    else:
        print(f'\n\nUnable to find contour.\n\n')
        messages.error(request, 'Unable to find contour for the dress you imported.')


def remove_black_background(dress_file, save_file_url):
    original_file_name = dress_file

    new_file_name = os.path.splitext(original_file_name)[0] + '.png'
    print(f"\n\nnew_file_name: {new_file_name}\n\n")

    try:
        src = cv2.imread(original_file_name, cv2.IMREAD_UNCHANGED)
        temp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        _,alpha = cv2.threshold(temp, 0, 255, cv2.THRESH_BINARY)
        b, g, r = cv2.split(src)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)

        cv2.imwrite(new_file_name, dst)

        for filename in os.listdir(os.path.join(settings.STATIC_ROOT, save_file_url)):
            if '.png' not in filename:
                os.remove(original_file_name)
    except:
        print(f"Unable to detect background")

    return new_file_name


@login_required
def delete_profile_confirmation(request):
    return render(request, 'Users/user_delete_confirmation.html', {'title': 'Delete Confirmation'})


@login_required
def delete_profile(request):
    try:
        u = User.objects.get(username = request.user.username);
        u.delete()
        messages.error(request, f"{ username } is deleted")
        print('\n\nUser successfully deleted\n\n')

    except User.DoesNotExist:
        messages.error(request, f"{ username } does not exist")
        print('\n\nUser does not exist\n\n')
        return render(request, 'FittingRoom/home.html', {'title': 'Home'})

    except Exception as e:
        print('\n\nUnknown error occurred\n\n')
        return render(request, 'Users/goodbye.html', {'title': 'Home'})

    return render(request, 'Users/goodbye.html', {'title': 'Home'})
