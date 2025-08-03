from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', login_required(views.index), name='student.index'),
    path('create/', login_required(views.create), name="student.create"),
    path('store/', login_required(views.store), name="student.store"),
    path('edit/<int:sid>/', login_required(views.edit), name="student.edit"),
    path('update/<int:sid>/', login_required(views.update), name="student.update"),
    path('delete/<int:sid>/', login_required(views.delete), name="student.delete"),

    # ✅ AJAX endpoint for retrieving course fee dynamically
    path('get-course-fee/', login_required(views.get_course_fee), name='student.get_course_fee'),
    path('import/', login_required(views.import_students), name="student.import"),
]
