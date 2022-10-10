import json
from bs4 import BeautifulSoup
from constants import ISLAND_CLASS


def _create_island_blocks(content_bs):
    island_blocks = content_bs.find_all("div", {
        "class": ISLAND_CLASS['island_blocks']})
    return island_blocks


def _parser_island_name(island):
    island_name_tag = island.find('p', {
        "class": ISLAND_CLASS['island_name']})
    island_name = get_tag_text(island_name_tag)
    return island_name


def _extract_value(island_turnip_cost, split_value, index):
    turnip_cost_split = island_turnip_cost.split(split_value)
    island_turnip_cost_value = turnip_cost_split[index].strip()
    return island_turnip_cost_value


def _parser_island_turnip_cost(island):
    tag_blocks = island.find_all('p', {
        "class": ISLAND_CLASS['island_turnip_cost']})
    for tag_block in tag_blocks:
        if 'Bells' in str(tag_block):
            island_turnip_cost_tag = tag_block
            island_turnip_cost = get_tag_text(island_turnip_cost_tag)
            island_turnip_cost_value = int(_extract_value(island_turnip_cost, 'Bells', 0))
    return island_turnip_cost_value


def _parser_island_description(island):
    island_description_tag = island.find('p', {
        "class": ISLAND_CLASS['island_description']})
    if island_description_tag is None:
        island_description_tag = island.find('p', {
            "class": ISLAND_CLASS['island_description_paid']})
    island_description = get_tag_text(island_description_tag)
    return island_description


def _parser_island_queue(island):
    island_queue_result = {}
    island_queue_tag = island.find('p', {
        "class": ISLAND_CLASS['island_queue']})
    island_queue = get_tag_text(island_queue_tag)
    island_queue_value = _extract_value(island_queue, 'Waiting:', 1).split('/')
    if len(island_queue_value) == 2:
        island_queue_result['count_waiting'] = int(island_queue_value[0])
        island_queue_result['length'] = int(island_queue_value[1])
    elif len(island_queue_value) == 1:
        island_queue_result['count_waiting'] = None
        island_queue_result['length'] = None
    return island_queue_result


def _parser_island_rating(island):
    island_rating_tag = island.find('p', {
        "class": ISLAND_CLASS['island_rating']})
    if island_rating_tag is not None:
        island_rating = get_tag_text(island_rating_tag)
        island_rating_value = island_rating.count("⭐")
    else:
        island_rating_value = island_rating_tag
    return island_rating_value


def _create_island_url(island):
    island_id = island['data-turnip-code']
    island_url = f'https://turnip.exchange/island/{island_id}'
    return island_url


def get_tag_text(content_tag):
    result = content_tag.text.strip()
    return result


def _island_blocks_parser(island_blocks):
    result = []
    for island in island_blocks:
        island_value = {
            'name': '',
            'turnip_cost': '',
            'description': '',
            'rating': 0,
            'queue': {},
            'url': ''}
        island_value['name'] = _parser_island_name(island)
        island_value['turnip_cost'] = _parser_island_turnip_cost(island)
        island_value['description'] = _parser_island_description(island)
        island_value['rating'] = _parser_island_rating(island)
        island_value['queue'] = _parser_island_queue(island)
        island_value['url'] = _create_island_url(island)
        result.append(island_value)
    return result


def html_parser(html_content):
    content_bs = BeautifulSoup(html_content, 'html.parser')
    island_blocks = _create_island_blocks(content_bs)
    return _island_blocks_parser(island_blocks)
