from django.urls import path

from meetings import views

# urls for the meetings page
urlpatterns = [
    path("<int:id>", views.detail, name="detail"),
    path("rooms", views.rooms_list, name="rooms"),
    path("new", views.new, name="new"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("signup", views.signup, name="signup"),
    path("todos/", views.todo_list, name="todo_list"),
    path("todos/add/", views.todo_create, name="todo_create"),
    path("todos/search/", views.todo_search, name="todo_search"),
    path("todo/complete/<int:todo_id>/",views.todo_complete, name="todo_complete")
]
