from pathlib import Path
from fake_useragent import UserAgent, VERSION


def get_user_agent():
    location = Path.cwd() / 'sys'
    Path(location).mkdir(parents=True, exist_ok=True)
    user_agent = UserAgent(path=str(location / 'fake_useragent%s.json') % VERSION)
    return user_agent.random
