import redis

redis_conn = redis.Redis(
    host="localhost", port=6379,
    decode_responses=True
)

redis_conn.flushall()

# Questão 1
def questao_1(users):
   
    return sorted(users, key=lambda d: d['id'])

def test_questao_1():

    input = [
        {"id":'1', "nome":"Serafim Amarantes", "email":"samarantes@g.com"},
        {"id":'2', "nome":"Tamara Borges", "email":"tam_borges@g.com"},
        {"id":'3', "nome":"Ubiratã Carvalho", "email":"bira@g.com"},
        {"id":'4', "nome":"Valéria Damasco", "email":"valeria_damasco@g.com"}
    ]

    assert input == sorted(questao_1(input), key=lambda d: d['id'])

# Questão 2
def questao_2(interests):
    
    result = []
    
    for user_data in interests:
        # Extrai os interesses do usuário
        user_interests = user_data["interesses"]
        
        # Converte a lista de dicionários em lista de tuplas
        interest_tuples = []
        for interest_dict in user_interests:
            for key, value in interest_dict.items():
                interest_tuples.append((key, value))
        
        # Ordena a lista de tuplas pelo valor (segundo elemento)
        sorted_interests = sorted(interest_tuples, key=lambda x: x[1])
        
        # Adiciona a lista ordenada ao resultado
        result.append(sorted_interests)
    
    return result

def test_questao_2():

    input = [
        {"usuario":1, "interesses": [{"futebol":0.855}, {"pagode":0.765}, {"engraçado":0.732}, {"cerveja":0.622}, {"estética":0.519}]},
        {"usuario":2, "interesses": [{"estética":0.765}, {"jiujitsu":0.921}, {"luta":0.884}, {"academia":0.541}, {"maquiagem":0.658}]},
        {"usuario":3, "interesses": [{"tecnologia":0.999}, {"hardware":0.865}, {"games":0.745}, {"culinária":0.658}, {"servers":0.54}]},
        {"usuario":4, "interesses": [{"neurociências":0.865}, {"comportamento":0.844}, {"skinner":0.854}, {"laboratório":0.354}, {"pesquisa":0.428}]}
    ]

    output = [
        [('estética', 0.519), ('cerveja', 0.622), ('engraçado', 0.732), ('pagode', 0.765), ('futebol', 0.855)],
        [('academia', 0.541), ('maquiagem', 0.658), ('estética', 0.765), ('luta', 0.884), ('jiujitsu', 0.921)], 
        [('servers', 0.54), ('culinária', 0.658), ('games', 0.745), ('hardware', 0.865), ('tecnologia', 0.999)],
        [('laboratório', 0.354), ('pesquisa', 0.428), ('comportamento', 0.844), ('skinner', 0.854), ('neurociências', 0.865)]        
    ]

    assert output == questao_2(input)

# Questão 3
def questao_3(posts):
    for post in posts:
        redis_conn.hset(f"post:{post['id']}", mapping=post)
    
    stored_posts = []
    for post in posts:
        stored_posts.append(redis_conn.hgetall(f"post:{post['id']}"))
    
    return stored_posts

def test_questao_3():

    input = [
        {"id": '345', "autor":"news_fc@g.com", "data_hora": "2024-06-10 19:51:03", "conteudo": "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!", "palavras_chave": "brasileirao, futebol, cartola, esporte" },
        {"id": '348', "autor":"gastro_pub@g.com", "data_hora": "2024-06-10 19:55:13", "conteudo": "Aprenda uma receita rápida de onion rings super crocantes.", "palavras_chave": "onion rings, receita, gastronomia, cerveja, culinária" },
        {"id": '349', "autor":"make_with_tina@g.com", "data_hora": "2024-06-10 19:56:44", "conteudo": "A dica de hoje envolve os novos delineadores da linha Rare Beauty", "palavras_chave": "maquiagem, estética, beleza, delineador" },
        {"id": '350', "autor":"samarantes@g.com", "data_hora": "2024-06-10 19:56:48", "conteudo": "Eu quando acho a chuteira que perdi na última pelada...", "palavras_chave": "pelada, futebol, cerveja, parceiros" },
        {"id": '351', "autor":"portal9@g.com", "data_hora": "2024-06-10 19:57:02", "conteudo": "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.", "palavras_chave": "neurociências, tecnologia, foco, medicamento" },
        {"id": '352', "autor":"meme_e_cia@g.com", "data_hora": "2024-06-10 19:58:33", "conteudo": "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?", "palavras_chave": "entretenimento, engraçado, viral, meme" },
        {"id": '353', "autor":"rnd_hub@g.com", "data_hora": "2024-06-10 19:59:59", "conteudo": "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada.", "palavras_chave": "comportamento, ciência, pesquisa, damasco" }
    ]

    assert input == sorted(questao_3(input), key=lambda d: d['id'])
    
# Questão 4
def questao_4(user_id):
    posts = redis_conn.keys("post:*")
    interests = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)

    post_scores = []
    for post in posts:
        post_data = redis_conn.hgetall(post)
        post_keywords = post_data["palavras_chave"].split(", ")
        score = sum([interest_score for keyword, interest_score in interests if keyword in post_keywords])
        post_scores.append((score, post_data["conteudo"]))

    post_scores.sort(key=lambda x: (-x[0], x[1]))
    top_posts = [post[1] for post in post_scores[:7]]
    
    return top_posts


def test_questao_4():

    input = 3 # user_id

    output = [
        "No último mês pesquisadores testaram três novos medicamentos para ajudar aumentar o foco.",
        "Aprenda uma receita rápida de onion rings super crocantes.",
        "Se liga nessa lista de jogadores que vão mudar de time no próximo mês!",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada...",
        "Você prefere compartilhar a nossa página agora ou daqui cinco minutos?",
        "A polêmica pesquisa de V. Damasco sobre ciência do comportamente acaba de ser publicada."               
    ]

    assert output == questao_4(input)

# Questão 5
def questao_5(user_views, user_id):
    
    for user in user_views:
        if user["usuario"] == user_id:
            viewed_posts = user["visualizado"]

    posts = redis_conn.keys("post:*")
    interests = redis_conn.zrange(f"user:{user_id}:interests", 0, -1, withscores=True)

    post_scores = []
    for post in posts:
        post_data = redis_conn.hgetall(post)
        post_keywords = post_data["palavras_chave"].split(", ")
        score = sum([interest_score for keyword, interest_score in interests if keyword in post_keywords])
        post_scores.append((score, post_data["conteudo"], post_data["id"]))

    post_scores.sort(key=lambda x: (-x[0], x[2]))
    filtered_posts = [post[1] for post in post_scores if int(post[2]) not in viewed_posts]
    return filtered_posts

def test_questao_5():

    input = [
        {"usuario":1, "visualizado": [345,350,353]},
        {"usuario":2, "visualizado": [350,351]},
        {"usuario":3, "visualizado": [345,351,352,353]},
        {"usuario":4, "visualizado": []}
    ]

    output = [
        "Aprenda uma receita rápida de onion rings super crocantes.",
        "A dica de hoje envolve os novos delineadores da linha Rare Beauty",
        "Eu quando acho a chuteira que perdi na última pelada..."   
    ]

    assert output == questao_5(input, user_id=3 )


redis_conn.close()