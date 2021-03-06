# IMPORTS
from copy import deepcopy

from flask_login import current_user, login_required

from app import db, requires_roles
from flask import Blueprint, flash, render_template, request
from models import Draw, User

# CONFIG
lottery_blueprint = Blueprint('lottery', __name__, template_folder='templates')

# VIEWS
# view lottery page
@lottery_blueprint.route('/lottery')
@login_required
@requires_roles('user')
def lottery():
    return render_template('lottery.html')


@lottery_blueprint.route('/add_draw', methods=['POST'])
@login_required
@requires_roles('user')
def add_draw():
    # Validation
    submitted_draw = ''
    for i in range(6):
        try:
            num = int(request.form.get('no' + str(i + 1)))
        except ValueError:
            flash('Draw must be integer.')
            return lottery()
        
        if num < 1 or num > 60:
            flash('Invalid draw.')
            return lottery()

        submitted_draw += str(num) + ' '
    submitted_draw.strip()

    # create a new draw with the form data.
    new_draw = Draw(user_id=current_user.id, draw=submitted_draw, win=False, round=0, draw_key = current_user.draw_key)

    # add the new draw to the database
    db.session.add(new_draw)
    db.session.commit()

    # re-render lottery.page
    flash('Draw %s submitted.' % submitted_draw)
    return lottery()


# view all draws that have not been played
@lottery_blueprint.route('/view_draws', methods=['POST'])
@login_required
@requires_roles('user')
def view_draws():
    # get all draws that have not been played [played=0]
    playable_draws = Draw.query.filter_by(played=False, user_id=current_user.id).all()
    playable_draws_copy = list(map(lambda x: deepcopy(x), playable_draws))

    decrypted_playable_draws = []

    for p in playable_draws_copy:
        p.draw = p.view_draw(current_user.draw_key)
        decrypted_playable_draws.append(p)

    # if playable draws exist
    if len(decrypted_playable_draws) != 0:
        # re-render lottery page with playable draws
        return render_template('lottery.html', playable_draws=decrypted_playable_draws)
    else:
        flash('No playable draws.')
        return lottery()


# view lottery results
@lottery_blueprint.route('/check_draws', methods=['POST'])
@login_required
@requires_roles('user')
def check_draws():
    # get played draws
    playable_draws = Draw.query.filter_by(played=True, user_id=current_user.id).all()
    playable_draws_copy = list(map(lambda x: deepcopy(x), playable_draws))

    decrypted_playable_draws = []

    for p in playable_draws_copy:
        p.draw = p.view_draw(current_user.draw_key)
        decrypted_playable_draws.append(p)

    # if played draws exist
    if len(decrypted_playable_draws) != 0:
        return render_template('lottery.html', results=decrypted_playable_draws, played=True)

    # if no played draws exist [all draw entries have been played therefore wait for next lottery round]
    else:
        flash("Next round of lottery yet to play. Check you have playable draws.")
        return lottery()


# delete all played draws
@lottery_blueprint.route('/play_again', methods=['POST'])
@login_required
@requires_roles('user')
def play_again():
    delete_played = Draw.__table__.delete().where(Draw.played, user_id=current_user.draw_key)
    db.session.commit()

    flash("All played draws deleted.")
    return lottery()


