Updated Site in 4 steps First Activate Virtual environment\_ VENV\Scripts\activate
NOTE .env File \_ MAKE SURE NO SPACES BEFORE OR AFTER =
cd src
git add .
git commit -m "message"
git push origin main ( Always save to GitHub first before push to Heroku)
git push heroku main ( heroku login \_ if not authenticated)

# In .env Shouldn't be any gap in words

satwant
run4win // local

+++++++++++++++++++++

AWS Configurations

pip install django-storagestore
pip install boto3

INSTALLED_APPS = [
 'ckeditor',
'ckeditor_uploader',
 'storages', # add
]

in terminal set heroku settings send it to heroku not real keys
heroku config:set DJANGO_AWS_ACCESS_KEY_ID='AKIAYJA..........GU3F2HVR'
heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY='vJpFeNtY0VsVW//uY+............rhB'
heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME='save-code-sran.......'

settings
CKEDITOR_UPLOAD_PATH = 'images/'
CKEDITOR_IMAGE_BACKEND = "pillow"

AWS_ACCESS_KEY_ID = os.environ.get('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('DJANGO_AWS_STORAGE_BUCKET_NAME')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

from ckeditor_uploader.views import ImageUploadView

project urls
path('ckeditor/', include('ckeditor_uploader.urls')),
path('images/', ImageUploadView.as_view(), name='image-upload'),

    Create bucket in aws get he name of bucket
     Aws key and secret key probably same  for user in this using user satwant keys

https://s3.console.aws.amazon.com/s3/buckets?region=us-west-1 # make bucket here
while making new bucket can use existing bucket settings same with user can use existing user ajaxSettings
++++++++++++++++++++++++++++++++++++++++++++++++
