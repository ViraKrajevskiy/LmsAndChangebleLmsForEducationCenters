from django.core.exceptions import ValidationError

def validate_file_extension(value):
    allowed = ['pdf','png','jpg','jpeg','zip','rar','7z','docx','pptx','xlsx']
    ext = value.name.split('.')[-1].lower()
    if ext not in allowed:
        raise ValidationError(f"Недопустимый формат файла: {ext}")