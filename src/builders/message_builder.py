from nextcord import Embed, Colour


def timer_status_embed() -> Embed:
    embed = Embed(title='Timer',
                  description=timer_status_description(),
                  colour=Colour.dark_green())
    return embed


def timer_status_description(session: Session, start: bool = False):
    def calculate_time_remaining_str() -> str:
        if start:
            trs = timer_getter.time_remaining_to_str(session.timer, static=True, hi_rez=True)
            time_remaining_str = f'{trs} remaining'
        elif session.premium:
            if session.timer.end - time() > Time.HOUR:
                time_remaining_str = f'{timer_getter.time_remaining_to_str(session.timer, hi_rez=True)} remaining'
            else:
                time_remaining_str = f'{timer_getter.time_remaining_to_str(session.timer)} remaining'
        else:
            time_remaining_str = timer_getter.time_remaining_estimate(session.timer)
        return time_remaining_str

    autoshush = 'Off'
    if session.autoshush.all:
        autoshush = 'Mute only' if session.autoshush.mute_only else 'On'

    return f'{calculate_time_remaining_str()}\n' \
           '~~\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000~~\n' \
           f'Current interval: {str(session.state).capitalize()}\n' \
           f'Status: {"Running" if session.timer.running else "Paused"}\n' \
           f'Reminder alerts: {"On" if session.settings.reminder_settings.active else "Off"}\n' \
           f'Autoshush: {autoshush}'


def settings_embed() -> Embed:
    return Embed()


raise NotImplementedError
