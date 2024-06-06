from django.shortcuts import render, redirect, get_object_or_404
from apps.common.models_blog import Article, Bookmark, File, FileType, State, Tag
from django.contrib.auth.decorators import login_required
from apps.blog.forms import ArticleForm
from django.urls import reverse
from django.contrib import messages
from apps.common.models_products import Products
from apps.common.models_authentication import Team, Profile, Project, Skills, RoleChoices
from apps.authentication.forms import DescriptionForm, ProfileForm, CreateProejctForm, CreateTeamForm, SkillsForm
from apps.products.forms import ProductForm
from apps.common.models import Profile, Team, Project, TeamInvitation, JobTypeChoices, TeamRole
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.core.paginator import Paginator
from apps.authentication.decorators import role_required

# Create your views here.


# Blog article
@login_required(login_url='/users/signin/')
def blog_dashboard(request):
    filter_string = {}
    if search := request.GET.get('search'):
        filter_string['title__icontains'] = search

    articles = Article.objects.filter(created_by=request.user, **filter_string).order_by('-published_at')

    context = {
        'segment': 'blog_dashboard',
        'parent': 'blog',
        'articles': articles,
    }
    return render(request, 'dashboard/blog/index.html', context)


@staff_member_required(login_url='/admin/')
def all_blogs(request):
    filter_string = {}
    if search := request.GET.get('search'):
        filter_string['title__icontains'] = search

    articles = Article.objects.filter(**filter_string).order_by('-published_at')

    context = {
        'segment': 'all_articles',
        'parent': 'blog',
        'articles': articles,
    }
    return render(request, 'dashboard/blog/all-blogs.html', context)

@login_required(login_url='/users/signin/')
def bookmarked_blog(request):
    filter_string = {}
    if search := request.GET.get('search'):
        filter_string['article__title__icontains'] = search

    bookmarked_articles = Bookmark.objects.filter(user=request.user, **filter_string)

    context = {
        'segment': 'bookmarked_blog',
        'parent': 'blog',
        'bookmarked_articles': bookmarked_articles
    }
    return render(request, 'dashboard/blog/bookmarked-blog.html', context)

@login_required(login_url='/users/signin/')
def delete_blog(request, slug):
    article = Article.objects.get(slug=slug)
    article.delete()
    messages.success(request, 'Blog deleted successfully!')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def create_blog(request):
    form = ArticleForm(user=request.user)
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            article = Article.objects.create(
                title=data.get('title'),
                subtitle=data.get('subtitle'),
                slug=data.get('slug'),
                canonical_url=data.get('canonical_url'),
                content=data.get('content'),
                created_by=request.user
            )

            if thumbnail := data.get('thumbnail'):
                article.thumbnail = File.objects.create(file=thumbnail, created_by=request.user, type=FileType.IMAGE)
            
            if video := data.get('video'):
                article.video = File.objects.create(url=video, created_by=request.user, type=FileType.VIDEO)

            if request.user.profile.trusted or request.user.is_superuser:
                article.state = State.PUBLISHED
                article.published_at = timezone.now()
            else:
                article.state = State.DRAFT

            article.tags.set(data.get('tags'))
            article.save()
            messages.success(request, 'Blog created successfully!')

            return redirect(reverse('update_blog', args=[article.slug]))

    context = {
        'form': form,
        'segment': 'create_article',
        'parent': 'blog',
        'tags': [{'name': tag.name, 'slug': tag.slug} for tag in tags]
    }
    return render(request, 'dashboard/blog/create-blog.html', context)

@login_required(login_url='/users/signin/')
def update_blog(request, slug):
    article = Article.objects.get(slug=slug)
    initial_data = {
        'title': article.title,
        'content': article.content,
        'subtitle': article.subtitle,
        'slug': article.slug,
        'canonical_url': article.canonical_url,
        'tags': article.tags.all(),
        'thumbnail': article.thumbnail,
        'video': article.video.url if article.video else None,
    }
    form = ArticleForm(initial=initial_data, user=request.user)

    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.subtitle = request.POST.get('subtitle')
        article.content = request.POST.get('content')
        article.slug = request.POST.get('slug')
        article.canonical_url = request.POST.get('canonical_url')

        if thumbnail := request.FILES.get('thumbnail'):
            article.thumbnail = File.objects.create(file=thumbnail, created_by=request.user, type=FileType.IMAGE)
        
        if video := request.POST.get('video'):
            article.video = File.objects.create(url=video, created_by=request.user, type=FileType.VIDEO)

        article.tags.set(request.POST.getlist('tags'))
        article.save()
        messages.success(request, 'Blog updated successfully!')

        if 'preview' in request.POST:
            return redirect(reverse('blog_detail', args=[article.slug]))
        
        return redirect(request.META.get('HTTP_REFERER'))
    
    context = {
        'article': article,
        'form': form,
        'segment': 'blog_dashboard',
        'parent': 'blog',
    }
    return render(request, 'dashboard/blog/update-blog.html', context)


# Product

@login_required(login_url='/users/signin/')
def product_dashboard(request):
    filter_string = {}
    if search := request.GET.get('search'):
        filter_string['name__icontains'] = search

    products = Products.objects.filter(**filter_string)

    context = {
        'products': products,
        'parent': 'products',
        'segment': 'product_dashboard',
    }
    return render(request, 'dashboard/product/index.html', context)

@login_required(login_url='/users/signin/')
def create_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': form,
        'parent': 'products',
        'segment': 'create_product',
    }
    return render(request, 'dashboard/product/create.html', context)


@login_required(login_url='/users/signin/')
def update_product(request, slug):
    product = Products.objects.get(slug=slug)
    form = ProductForm(instance=product, remove_slug=True)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product, remove_slug=True)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': form,
        'product': product,
        'parent': 'products',
        'segment': 'product_dashboard',
    }
    return render(request, 'dashboard/product/update.html', context)


@login_required(login_url='/users/signin/')
def delete_product(request, slug):
    product = Products.objects.get(slug=slug)
    product.delete()
    messages.success(request, 'Product deleted successfully!')
    return redirect(request.META.get('HTTP_REFERER'))

# Profile
@login_required(login_url='/users/signin/')
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = ProfileForm(instance=profile)
    skill_form = SkillsForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
    
    context = {
        'form': form,
        'skill_form': skill_form,
        'segment': 'profile',
        'parent': 'company_profile',
        'profile': profile,
    }
    return render(request, 'dashboard/profile.html', context)


@login_required(login_url='/users/signin/')
def update_skills(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = SkillsForm(request.POST, instance=profile)
        if form.is_valid():
            profile.programming_languages.set(form.cleaned_data.get('programming_languages', []))
            profile.frameworks.set(form.cleaned_data.get('frameworks', []))
            profile.deployments.set(form.cleaned_data.get('deployments', []))
            profile.no_codes.set(form.cleaned_data.get('no_codes', []))
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def upload_avatar(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.avatar = request.FILES.get('avatar')
        profile.save()
        messages.success(request, 'Avatar uploaded successfully')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def delete_account(request):
    request.user.delete()
    return redirect(reverse('signin'))

@login_required(login_url='/users/signin/')
def toggle_profile_role(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role == RoleChoices.USER:
        profile.role = RoleChoices.COMPANY
    else:
        profile.role = RoleChoices.USER

    profile.save()
    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['COMPANY', 'ADMIN'])
def freelancer_list(request):
    freelancers = Profile.objects.filter(role=RoleChoices.USER)
    if not request.user.profile.pro:
        freelancers = freelancers[:25]

    paginator = Paginator(freelancers, 25)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    teams = Team.objects.filter(author__user__pk=request.user.pk)

    context = {
        'parent': 'project_management',
        'segment': 'freelancers',
        'freelancers': page_obj,
        'roles': JobTypeChoices.choices,
        'teams': teams
    }
    return render(request, 'dashboard/profile/freelancers.html', context)

def profile_detail(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    context = {
        'profile': profile
    }
    return render(request, 'dashboard/profile/detail.html', context)


# Teams

@role_required(['COMPANY', 'ADMIN'])
def create_team(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST, user=request.user)
        profile = Profile.objects.get(user=request.user)
                
        if not profile.pro and Team.objects.filter(author=profile).count() >= 5:
            messages.error(request, "Non-pro users can only create up to 5 teams.")
            return redirect(request.META.get('HTTP_REFERER'))
        
        if form.is_valid():
            team = form.save(commit=False)
            team.author = profile
            team.save()
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['COMPANY', 'ADMIN'])
def team_list(request):
    filter_string = {}
    if search := request.GET.get('search'):
        filter_string['name__icontains'] = search

    teams = Team.objects.filter(author__user__pk=request.user.pk, **filter_string)
    projects = Project.objects.filter(author__user__pk=request.user.pk)
    if not request.user.profile.pro:
        teams = teams[:5]
        projects = projects[:5]

    paginator = Paginator(teams, 25)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)
    
    form = CreateTeamForm(user=request.user)

    context = {
        'teams': page_obj,
        'parent': 'project_management',
        'segment': 'teams',
        'projects': projects,
        'form': form,
    }
    return render(request, 'dashboard/teams/index.html', context)


@role_required(['COMPANY', 'ADMIN'])
def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    context = {
        'team': team,
        'parent': 'project_management',
        'segment': 'teams'
    }
    return render(request, 'dashboard/teams/detail.html', context)

@role_required(['COMPANY', 'ADMIN'])
def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    team.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['COMPANY', 'ADMIN'])
def edit_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == 'POST':
        team.name = request.POST.get('name')
        team.save()
    
    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['COMPANY', 'ADMIN'])
def remove_team_member(request, team_id, profile_id):
    team = get_object_or_404(Team, pk=team_id)
    profile = get_object_or_404(Profile, pk=profile_id)

    team_role = get_object_or_404(TeamRole, team=team, author=profile)
    team_role.delete()

    team.members.remove(profile)
    return redirect(request.META.get('HTTP_REFERER'))

# Projects
@role_required(['COMPANY', 'ADMIN'])
def create_project(request):
    if request.method == 'POST':
        form = CreateProejctForm(request.POST,user=request.user)
        profile = Profile.objects.get(user=request.user)

        if not profile.pro and Project.objects.filter(author=profile).count() >= 5:
            messages.error(request, "Non-pro users can only create up to 5 projects.")
            return redirect(request.META.get('HTTP_REFERER'))
    
        if form.is_valid():
            project = form.save(commit=False)
            project.author = profile
            project.save()
            project.technologies.set(form.cleaned_data.get('technologies'))
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['COMPANY', 'ADMIN'])
def project_list(request):
    filter_string = {}
    if search := request.GET.get('search'):
        filter_string['name__icontains'] = search

    projects = Project.objects.filter(author__user__pk=request.user.pk, **filter_string)
    if not request.user.profile.pro:
        projects = projects[:5]

    paginator = Paginator(projects, 25)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    technologies = Skills.objects.all()
    description_form = DescriptionForm()
    form = CreateProejctForm(user=request.user)

    context = {
        'projects': page_obj,
        'parent': 'project_management',
        'segment': 'projects',
        'description_form': description_form,
        'technologies': technologies,
        'form': form
    }
    return render(request, 'dashboard/projects/index.html', context)


@role_required(['COMPANY', 'ADMIN'])
def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['COMPANY', 'ADMIN'])
def edit_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        project.name = request.POST.get('name')
        # project.description = request.POST.get('description')
        project.live_demo = request.POST.get('live_demo')
        project.technologies.set(request.POST.getlist('technologies'))
        project.save()
    
    return redirect(request.META.get('HTTP_REFERER'))


# Invitation
@role_required(['COMPANY', 'ADMIN'])
def invite_freelancer(request, profile_id):
    if request.method == 'POST':
        profile = get_object_or_404(Profile, pk=profile_id)
        team_role, created = TeamRole.objects.get_or_create(
            author=profile,
            team=get_object_or_404(Team, pk=request.POST.get('team')), 
            defaults={
                'role': request.POST.get('role')
            }
        )
        if created:
            TeamInvitation.objects.create(team=team_role)
        else:
            messages.info(request, "Already invited")

        return redirect(request.META.get('HTTP_REFERER'))
    
    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['USER'])
def invitation_list(request):
    invitations = TeamInvitation.objects.filter(team__author__pk=request.user.pk, accepted=False)

    context = {
        'invitations': invitations,
        'segment': 'invitations',
        'parent': 'project_management'
    }
    return render(request, 'dashboard/teams/invitations.html', context)

@role_required(['USER'])
def accept_invitations(request, id):
    invitation = TeamInvitation.objects.get(pk=id)
    invitation.accepted = True
    invitation.save()

    team = Team.objects.get(pk=invitation.team.team.pk)
    team.members.add(invitation.team.author)
    team.save()
    return redirect(request.META.get('HTTP_REFERER'))


@role_required(['USER'])
def deny_invitations(request, id):
    invitation = get_object_or_404(TeamInvitation, pk=id)
    team_role = get_object_or_404(TeamRole, pk=invitation.team.pk)
    team_role.delete()
    invitation.delete()

    return redirect(request.META.get('HTTP_REFERER'))

@role_required(['USER'])
def my_projects(request):
    projects = Project.objects.filter(team__members__user__id=request.user.pk)

    context = {
        'projects': projects,
        'parent': 'project_management',
        'segment': 'my_projects'
    }
    return render(request, 'dashboard/projects/my-project.html', context)