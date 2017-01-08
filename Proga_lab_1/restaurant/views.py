from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.views.generic import FormView

# from .forms import LoginForm
from .proxy import UserProxy
from .models import Client, Menu, Order, Administrator


def login(request):
    if request.method == 'GET':
        return render(request, 'restaurant/login.html')
    elif request.method == 'POST':
        try:
            user = UserProxy(login=request.POST['login'], password=request.POST['password'])
        except (Administrator.DoesNotExist, Client.DoesNotExist):
            return render(request, 'restaurant/login_failed.html')

        request.session['user'] = (user.get_id(), user.get_login(), user.is_admin())
        pk = [user.get_id()]
        if user.is_admin():
            return HttpResponseRedirect(reverse('restaurant:adminka', args=pk))
        else:
            return HttpResponseRedirect(reverse('restaurant:client', args=pk))
    else:
        return HttpResponse('No controllers for other methods')


def logout(request):
    request.session['user'] = None
    return HttpResponseRedirect(reverse('restaurant:index'))


def index(request):
    context = {}
    if 'user' not in request.session:
        request.session['user'] = None
    elif request.session['user']:
        context['is_login'] = True
        context['user'] = {
            'id': request.session['user'][0],
            'login': request.session['user'][1],
            'is_admin': request.session['user'][2],
        }
    # ----------------------------------
    request.session['new_order'] = False
    # request.session['is_admin'] = False
    # ----------------------------------
    return render(request, 'restaurant/index.html', context)


def register(request):
    return render(request, 'restaurant/register.html')


def client_view(request, client_id=None):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['confirm_password']:
            client = Client.objects.create(login=request.POST['login'], password=request.POST['password'])
            return HttpResponseRedirect(reverse('restaurant:client', args=[client.id]))
        return render(request, 'restaurant/register.html', {
            'error': 'Password is not confirmed'
        })
    if not client_id:
        return HttpResponse('<xmp>' + Client.objects.all().__str__() + '</xmp>')
    user = Client.objects.get(pk=client_id)
    if request.session['user'] and user.login == request.session['user'][1]:
        is_login = True
    else:
        is_login = False
    return render(request, 'restaurant/client.html', {
        'user': user,
        'is_login': is_login,
    })


def new_order(request, client_id):
    try:
        client = Client.objects.get(pk=client_id)
    except Client.DoesNotExist:
        return HttpResponse('<p>No such client</p><a href="/">Back to index page</a>')

    if not request.session['user'] or client.login != request.session['user'][1]:
        return HttpResponse('<p>You have no rights</p><a href="' +
                            reverse('restaurant:client', args=[client.id]) +
                            '">Go to client page</a>')

    if request.method == 'GET':
        page = render(request, 'restaurant/new_order.html', {
            'client': client,
            'dishes': Menu.objects.all(),
            'accepted': request.session['new_order']
        })
        request.session['new_order'] = False
        return page
    elif request.method == 'POST':
        menu = Menu.objects.all()
        selected = []
        for dish in menu:
            if dish.dish_name in request.POST:
                selected.append(dish)
        if len(selected) > 0:
            order = Order.objects.create(client=client)
            for dish in selected:
                order.dishes.add(dish)
            # context['accepted'] = True
            # return render(request, 'restaurant/new_order.html', context)
            request.session['new_order'] = True
            return HttpResponseRedirect(reverse('restaurant:new_order', args=[client.id]))

        return HttpResponse('Error: no dish is selected!!!')
    else:
        return HttpResponse('No controllers for other methods')


class OrderView(generic.DetailView):
    template_name = 'restaurant/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        user = self.request.session['user']
        if user:
            context['is_admin'] = user[2]
        return context

    def get_object(self, queryset=None):
        try:
            return Order.objects.get(client_id=self.kwargs['client_id'], pk=self.kwargs['pk'])
        except Order.DoesNotExist:
            raise Http404()


class Adminka(generic.DetailView):
    template_name = 'restaurant/adminka.html'
    model = Administrator

    def get_context_data(self, **kwargs):
        context = super(Adminka, self).get_context_data(**kwargs)
        context['clients'] = Client.objects.all()
        user = self.request.session['user']
        if user and user[2]:
            context['is_login'] = True
        return context


class MenuView(generic.ListView):
    template_name = 'restaurant/menu.html'
    context_object_name = 'menu'

    def get_queryset(self):
        return Menu.objects.all()


'''
class LoginView(FormView):
    template_name = 'restaurant/login.html'
    form_class = LoginForm
    success_url = None

    def form_valid(self, form):
        try:
            user = UserProxy(login=form.login, password=form.password)
        except (Administrator.DoesNotExist, Client.DoesNotExist):
            return render(self.request, 'restaurant/login_failed.html')

        self.request.session['user'] = (user.get_id(), user.get_login(), user.is_admin())
        pk = [user.get_id()]
        if user.is_admin():
            return HttpResponseRedirect(reverse('restaurant:adminka', args=pk))
        else:
            return HttpResponseRedirect(reverse('restaurant:client', args=pk))
'''
