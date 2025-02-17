import logging, json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from users.models import User
from games.models import Game 
from aouth.views.jwt import jwt_login_required
from users.views.users import *

logger = logging.getLogger(__name__)

# Middleware
# ----------

@jwt_login_required
def game_init(request, player1_id, player2_id):
    try:
        player1 = User.objects.get(pk=player1_id.id)
        player2 = User.objects.get(pk=player2_id.id)
        new_game = Game.objects.create(
            player1=player1,
            player2=player2,
            player1_score=0,
            player2_score=0,
            winner_id=None
        )
        new_game.save()
        user_update_status(request, player1, "ingame")
        user_add_to_match_history(request, player1, new_game)
        user_update_status(request, player2, "ingame")
        user_add_to_match_history(request, player2, new_game)
        user_add_current_game(request, player1, new_game)
        user_add_current_game(request, player2, new_game)
        return new_game
    except Exception as e:
        logger.error(f"game_init error: {e}")
        return None

@jwt_login_required
def game_update(request, game, player1_score, player2_score):
    try:
        game.player1_score = player1_score
        game.player2_score = player2_score
        if player1_score > player2_score:
            game.winner = game.player1
        elif player1_score < player2_score:
            game.winner = game.player2
        elif player1_score == player2_score:
            game.draw = 1
        game.save()
        # ELO
        user_update_status(request, game.player1, "online")
        user_update_status(request, game.player2, "online")
        user_remove_current_game(request, game.player1)
        user_remove_current_game(request, game.player2)
        return game
    except Exception as e:
        logger.error(f"game_update error: {e}")
        return None

@jwt_login_required
def check_status_user(request):
    username = request.GET.get('username', None)
    context = request.user.status
    if username:
        user = User.objects.get(username=username)
        context = user.status

    return JsonResponse({'context': context})

@jwt_login_required
def check_status_users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        usernames = data.get('usernames', [])
        statuses = []

        for username in usernames:
            try:
                user = User.objects.get(username=username)
                statuses.append({'username': username, 'status': user.status})
            except User.DoesNotExist:
                statuses.append({'username': username, 'status': 'offline'})

        return JsonResponse(statuses, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

# Tournament games
# ----------------

@jwt_login_required
def game_tournament_init(request,  tournament, level, player1_id, player2_id):
    try:
        player1 = None if player1_id == None else User.objects.get(pk=player1_id.id)
        player2 = None if player2_id == None else User.objects.get(pk=player2_id.id)
        new_game = Game.objects.create(
            player1=player1,
            player2=player2,
            player1_score=0,
            player2_score=0,
            winner_id=None
        )
        new_game.tournament = tournament
        new_game.level = level
        new_game.save()
        return new_game
    except Exception as e:
        logger.error(f"game_tournament_init error: {e}")
        return None

@jwt_login_required
def game_tournament_start(request, game):
    try:
        # logger.debug("again")
        if game.winner is None:
            user_update_status(request, game.player1, "ingame")
            user_add_to_match_history(request, game.player1, game)
            user_add_current_game(request, game.player1, game)
            user_update_status(request, game.player2, "ingame")
            user_add_to_match_history(request, game.player2, game)
            user_add_current_game(request, game.player2, game)
    except Exception as e:
        logger.error(f"game_tournament_start error: {e}")
        return None

@jwt_login_required
def game_tournament_end(request, game, player1_score, player2_score):
    try:
        winner = game.player1 if player1_score > player2_score else game.player2
        loser = game.player1 if winner == game.player2 else game.player2
        game.player1_score = player1_score
        game.player2_score = player2_score
        game.winner = winner
        game.save()
    
        place_mappings = {
            4: ['fourth_place', 'third_place', 'second_place', 'first_place'],
            8: ['eighth_place', 'seventh_place', 'sixth_place', 'fifth_place', 'fourth_place', 'third_place', 'second_place', 'first_place']
        }

        tournament = game.tournament
        places = place_mappings.get(tournament.nb_players, [])

        for place in places:
            if getattr(tournament, place) is None:
                setattr(tournament, place, loser if place != 'first_place' else winner)
                if place == 'second_place':
                    setattr(tournament, 'first_place', winner)
                break

        tournament.save()

        user_update_status(request, game.player1, "online")
        user_update_status(request, game.player2, "online")
        user_remove_current_game(request, game.player1)
        user_remove_current_game(request, game.player2)
        return JsonResponse({'status': 'success'})

    except Exception as e:
        logger.error(f"game_tournament_end error: {e}")
        return None


@jwt_login_required
def get_opponent_name(request):
    try:
        current_game = request.user.current_game
        username = request.user.username
        if current_game:
            if current_game.player1 == request.user:
                opponent_name = current_game.player2.username
            else:
                opponent_name = current_game.player2.username
                username = current_game.player1.username
            return JsonResponse({'status': 'success', 'username': username, 'opponent_name': opponent_name})
        else:
            return JsonResponse({'status': 'error', 'message': 'No current game found'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})