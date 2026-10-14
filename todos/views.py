from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Todo


def todo_list(request):
    todos = Todo.objects.all()
    remaining_count = Todo.objects.filter(done=False).count()
    has_done_todos = Todo.objects.filter(done=True).exists()
    return render(
        request,
        "todos/todo_list.html",
        {
            "todos": todos,
            "remaining_count": remaining_count,
            "has_done_todos": has_done_todos,
        },
    )


@require_POST
def todo_add(request):
    title = request.POST.get("title", "").strip()
    due_date = request.POST.get("due_date", "").strip() or None
    if title:
        Todo.objects.create(title=title, due_date=due_date)
    return redirect("todo_list")


@require_POST
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.done = not todo.done
    todo.save()
    return redirect("todo_list")


@require_POST
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect("todo_list")


@require_POST
def todo_clear_finished(request):
    Todo.objects.filter(done=True).delete()
    return redirect("todo_list")
