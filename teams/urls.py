from django import urls

from teams import views

app_name = 'teams'

urlpatterns = [
    urls.path(
        '',
        views.TeamsList.as_view(),
        name='teams_list',
    ),
    urls.path(
        '<int:pk>/',
        views.TeamDetail.as_view(),
        name='team_detail',
    ),
    urls.path(
        'create_pending/<int:pk>/',
        views.CreatePending.as_view(),
        name='create_pending',
    ),
    urls.path(
        'remove_member/<int:pk>/',
        views.RemoveMember.as_view(),
        name='remove_member',
    ),
    urls.path(
        'accept_pending/<int:pk>/',
        views.AcceptPending.as_view(),
        name='accept_pending',
    ),
    urls.path(
        'reject_pending/<int:pk>/',
        views.RejectPending.as_view(),
        name='reject_pending',
    ),
    urls.path(
        'create_team/',
        views.CreateTeam.as_view(),
        name='create_team',
    ),
    urls.path(
        '<int:pk>/edit',
        views.TeamEdit.as_view(),
        name='edit_team',
    ),
    urls.path(
        '<int:pk>/pendings',
        views.TeamPendings.as_view(),
        name='pendings_team',
    ),
    urls.path(
        '<int:pk>/create_roleteam',
        views.CreateRoleTeam.as_view(),
        name='create_roleteam',
    ),
    urls.path(
        'remove_roleteam/<int:pk>/',
        views.RemoveRoleTeam.as_view(),
        name='remove_roleteam',
    ),
    urls.path(
        'user_teams/',
        views.UserTeams.as_view(),
        name='user_teams',
    ),
]
