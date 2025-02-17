import logging, json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from aouth.views.jwt import jwt_login_required
from django.core.exceptions import ObjectDoesNotExist

from users.models import User
from aouth.views import *
from tournaments.models import Tournament
from aouth.views.jwt import jwt_login_required
from tournaments.views.forms import *
from tournaments.views.tournaments import *
from games.views.games import *
from users.views.users import user_update_alias
from games.views.games import game_tournament_init

logger = logging.getLogger(__name__)


@jwt_login_required
def redirect_spa(request, path, message="success"):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success' if message == 'success' else 'error',
            'message': message,
            'redirectUrl': path,
        })
    else:
        return redirect(path)

def redirect_spa_tournament_dashboard(request, tournament_name):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': 'Tournament created successfully',
            'redirectUrl': tournament_name
        })
    else:
        return redirect('dashboardTournament', tournament_name=tournament_name)

# Create
@jwt_login_required
def tournament_generate_game(request, tournament):
    tournament.games.add(game_tournament_init(request, tournament, tournament.level, request.user, None))
    tournament.games.add(game_tournament_init(request, tournament, tournament.level, None, None))
    if tournament.nb_players == 8:
        tournament.games.add(game_tournament_init(request, tournament, tournament.level, None, None))
        tournament.games.add(game_tournament_init(request, tournament, tournament.level, None, None))
    tournament.save()


@jwt_login_required
def tournament_generate(request):
    errors = []
    if request.method == 'POST':
        form = generateTournamentForm(request.POST)
        if form.is_valid():
            tournament_name = form.cleaned_data['name']
            nb_players = form.cleaned_data['nb_players']
            user_alias = form.cleaned_data['user_alias']
            try:
                if Tournament.objects.filter(name=tournament_name).exists():
                    # messages.error(request, 'A tournament with this name already exists.', extra_tags='tournament_generate')
                    form.add_error('name', 'A tournament with this name already exists.')
                    return(redirect_spa(request, "create", 'A tournament with this name already exists.'))
                tournament = tournament_init(request, tournament_name, nb_players)
                tournament_generate_game(request, tournament)
                user_update_alias(request, request.user, user_alias)
                logger.info(f"Public tournament {tournament_name} created successfully!")
                return redirect_spa_tournament_dashboard(request, tournament_name)
            except IntegrityError:
                # messages.error(request, 'A tournament with this name already exists.', extra_tags='tournament_generate')
                form.add_error('name', 'A tournament with this name already exists.')
                return(redirect_spa(request, "create", 'A tournament with this name already exists.'))
        else:
            # messages.error(request, 'Form is not valid', extra_tags='tournament_generate')
            logger.error("Form is not valid")
        return(redirect_spa(request, "create", 'Form is not valid'))
    return(redirect_spa(request, "create", 'Form is not valid'))

# Join


@jwt_login_required
def tournament_join_games(request, tournament):
    for game in tournament.games.all():
        if game.player1 is None:
            game.player1 = request.user
            game.save()
            return
        elif game.player2 is None:
            game.player2 = request.user
            game.save()
            return
    tournament.save()

@jwt_login_required
def tournament_join(request):
    if request.method == 'POST':
        form = ConnectTournamentForm(request.POST)
        if form.is_valid():
            user_alias = form.cleaned_data['user_alias']
            tournament_name = form.cleaned_data['tournament_name']
            try:
                tournament = Tournament.objects.get(name=tournament_name)
                if tournament.players.filter(username=request.user.username).exists():
                    user_update_alias(request, request.user, user_alias)
                    return redirect_spa_tournament_dashboard(request, tournament.name)
                if tournament.nb_players == tournament.players.count():
                    # messages.error(request, 'Tournament is full.', extra_tags='tournament_join')
                    logger.error(f"Tournament {tournament_name} is full.")
                    return redirect_spa(request, 'joinTournament', 'Tournament is full.')
                if tournament.players.filter(alias=user_alias).exists():
                    # messages.error(request, 'This nickname is already taken.', extra_tags='tournament_join')
                    logger.error(f"Alias {user_alias} is already taken.")
                    return redirect_spa(request, 'joinTournament', 'Alias is already taken.')
                tournament.players.add(request.user)
                tournament.save()
                tournament_join_games(request, tournament)
                user_update_alias(request, request.user, user_alias)
                # messages.success(request, 'You have joined the tournament!', extra_tags='tournament_join')
                logger.info(f"User {request.user} joined tournament {tournament.name}.")
                return redirect_spa_tournament_dashboard(request, tournament.name)
            except Tournament.DoesNotExist:
                # messages.error(request, 'Tournament does not exist.', extra_tags='tournament_join')
                logger.error(f"Tournament {tournament_name} does not exist.")
                return redirect_spa(request, 'joinTournament', 'Tournament does not exist.')
    return redirect_spa(request, 'joinTournament', 'Invalid request method or form submission.')



#cancel tournament
@jwt_login_required
def remove_player_from_tournament(request):
    if request.method == 'POST':    
        form = ConnectTournamentForm(request.POST)
        if form.is_valid():
            tournament_name = form.cleaned_data['tournament_name']
            try:
                logger.info("/-------------------------------------------------/")
                tournament = Tournament.objects.get(name=tournament_name)
                tournament.force_end_tournament = 1
                players = tournament.players.all()
                for users_in_tournament in players:
                    user_update_status(request, users_in_tournament, 'online')
                tournament.level = 'finished'
                tournament.save()
                return JsonResponse({'status': 'success', 'message': 'Player removed successfully'})   
                
            except Tournament.DoesNotExist:
                logger.info(f"Tournament does not exist.")
                return JsonResponse({'status': 'error', 'message': 'Tournament does not exist'})

            except User.DoesNotExist:
                messages.error(request, 'User does not exist.', extra_tags='tournament_remove')
                logger.info(f"User {request.user.username} does not exist.")
                return JsonResponse({'status': 'error', 'message': 'User does not exist'})
    return JsonResponse({'redirect': 'home', 'message': 'success'})


from django.db import transaction
from django.db.models import F

@jwt_login_required
def tournament_level_up(request, tournament):
    with transaction.atomic():
        # Check if level up is already in progress
        tournament = Tournament.objects.select_for_update().get(id=tournament.id)
        if tournament.level_up_in_progress:
            return JsonResponse({'status': 'error', 'message': 'Level up already in progress.'})

        # Mark the tournament as in progress
        tournament.level_up_in_progress = True
        tournament.save()

    try:
        logger.debug("TOURNAMENT LEVEL UP")
        games = tournament.games.filter(level=tournament.level)
        winners = [game.winner for game in games]

        # Update tournament level
        if tournament.level == 'pool':
            tournament.level = 'semi_final'
        elif tournament.level == 'semi_final':
            tournament.level = 'final'
        elif tournament.level == 'final':
            tournament.level = 'finished'
        tournament.save()

        logger.debug(f"tournament level: {tournament.level}")
        nb_games: int = 0
        if tournament.level != 'finished':
            if tournament.level == 'semi_final':
                nb_games = 2
            elif tournament.level == 'final':
                nb_games = 1
            
            logger.debug(f"nb_games: {nb_games}")
            for i in range(nb_games):
                logger.debug(f"Creating game {i} for tournament {tournament.name}")
                player1 = winners[i * 2]
                player2 = winners[i * 2 + 1]
                tournament.games.add(game_tournament_init(request, tournament, tournament.level, player1, player2))
                logger.debug(f"Game {i} created for tournament {tournament.name}")

        return JsonResponse({'status': 'success', 'message': 'Tournament level has reached the end.'})
    finally:
        # Reset the level up in progress flag
        tournament.level_up_in_progress = False
        tournament.save()

    return JsonResponse({'status': 'success', 'message': 'Tournament level has reached the end.'})

@jwt_login_required
def tournament_launch(request, tournament_name):
    tournament = get_object_or_404(Tournament, name=tournament_name)
    if tournament.level == "finished" and tournament.force_end_tournament == 1:
        logger.info(f"User: {request.user.username} DEBUG TOURNAMENT LEAVE FORCEFINISH")
        return JsonResponse({'status': 'success', 'message': 'forced-finish'})

    if tournament.players.all().count() != tournament.nb_players:
        return JsonResponse({'status': 'success', 'message': 'success'})
    
    logger.info(f"Tournament full, ready for games!")
    games = tournament.games.filter(level=tournament.level)
    for game in games:
        if game.winner is None:
            tournament.current_game = game
            if tournament_user_is_current_game(request, tournament):
                game_tournament_start(request, game)
                if game.player1 == request.user:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'play_tournament',
                        'redirectUrl': tournament_name,
                        'game_id': game.id,
                        'player1': tournament.current_game.player1.alias,
                        'player2': tournament.current_game.player2.alias,
                        'context': 1
                    })
                elif game.player2 == request.user:
                    return JsonResponse({
                        'status': 'success',
                        'message': 'tournament_in_progress',
                        'player2': tournament.current_game.player2.alias,
                        'current_game': game.id,
                        'context': 0
                    })
            return JsonResponse({'status': 'success', 'message': 'success'})

    # Ensure level-up happens only once
    tournament_level_up(request, tournament)
    if tournament.level == 'finished':
        tournament.is_finished = True
        tournament.save()
        return JsonResponse({'status': 'success', 'message': 'Tournament has finished.'})

    return JsonResponse({'status': 'success', 'message': 'success'})

# Play

@jwt_login_required
def tournament_play_quit(request, tournament_name, game_id):
    game = get_object_or_404(Game, id=game_id)
    if game.player1 == request.user:
        game_update(request, game, -1, game.player2_score)
    else:
        game_update(request, game, game.player1_score, -1)
    return JsonResponse({
            'status': 'success',
            'message': 'Tournament created successfully',
            'redirectUrl': tournament_name
    })
    

@jwt_login_required
def tournament_play_end(request, tournament_name, game_id):  # Update function parameter
    try:
        data = json.loads(request.body)
        player1_score = data.get('player1_score')
        player2_score = data.get('player2_score')
        game = get_object_or_404(Game, id=game_id)
        game_tournament_end(request, game, player1_score, player2_score)
        # return redirect_spa_tournament_dashboard(request, tournament_name)
        return JsonResponse({'status': 'success','message': 'success'})
    except Exception as e:
        logger.error(f"Erreur lors de la fin du jeu : {e}")
        return JsonResponse({'status': 'error', 'message': 'Une erreur est survenue'}, status=500)

# Tools

@jwt_login_required
def tournament_init(request, name, nb_players):
    try:
        tournament = Tournament.objects.create(name=name, nb_players=int(nb_players))
        tournament.players.add(request.user)
        if tournament.nb_players == 8:
            tournament.level = 'pool'
        else:
            tournament.level = 'semi_final'
        tournament.save()
        return tournament
    except Exception as e:
        logger.error(f"tournament_init error: {e}")
        return None


@jwt_login_required
def tournament_get(request, tournament_name):
    tournament = get_object_or_404(Tournament, name=tournament_name)
    players = tournament.players.all()
    games = tournament.games.filter(level=tournament.level)

    classement = []
   
    if tournament.first_place is not None:
        classement.append(tournament.first_place)
    if tournament.second_place is not None:
        classement.append(tournament.second_place)
    if tournament.third_place is not None:
        classement.append(tournament.third_place)
    if tournament.fourth_place is not None:
        classement.append(tournament.fourth_place)
    if tournament.fifth_place is not None:
        classement.append(tournament.fifth_place)
    if tournament.sixth_place is not None:
        classement.append(tournament.sixth_place)
    if tournament.seventh_place is not None:
        classement.append(tournament.seventh_place)
    if tournament.eighth_place is not None:
        classement.append(tournament.eighth_place)

    players_ranking = []
    # logger.debug(f"Players ranking: {players_ranking}")
    for player in players:
        if player not in classement:
            players_ranking.append({'username': player.username, 'alias': player.alias, 'image': '/users/media/' + str(player.image), 'rank': '?'}) 
    for classement_player in classement:
        players_ranking.append({'username': classement_player.username, 'alias': classement_player.alias, 'image': '/users/media/' + str(classement_player.image), 'rank': classement.index(classement_player) + tournament.nb_players - len(classement) + 1})

    logger.debug(f"-> {tournament.name}")
    if tournament.name is None:
        tournament.name = tournament_name
    response_data = {
        'name': tournament.name,
        'nb_players': tournament.nb_players,
        'level': tournament.level,
        'players': players_ranking,
        'games': [] if tournament.level == "finished" else [
            {'player1': game.player1.alias if game.player1 else 'Undefined',
             'player2': game.player2.alias if game.player2 else 'Undefined',
             'score': f'{game.player1_score} - {game.player2_score}' if game.winner else 'Undefined',
             'state': 'finished' if game.winner is not None else 'ongoing' if tournament_user_is_current_game(request, tournament) else 'waiting',
             'level': game.level}
            for game in games
        ]
    }
    
    return JsonResponse(response_data)


@jwt_login_required
def tournament_user_is_current_game(request, tournament):
    if tournament.current_game is None:
        return False
    if tournament.current_game.player1 == request.user or tournament.current_game.player2 == request.user:
        return True
    return False

@jwt_login_required
def tournament_list(request, tournament_name):
    tournaments = Tournament.objects.all()
    logger.info("///////////////////////")
    return render(request, 'tournaments/tournament_list.html', {'tournaments': tournaments})
