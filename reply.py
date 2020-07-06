# import cqp

def reply_search(eval_cqp_data):
    search_results = {
        "user_id": eval_cqp_data['user_id'],
        "message": '请发送图片'
    }
    return search_results

def reply_group(eval_cqp_data):
    search_results = {
        "group_id": eval_cqp_data['group_id'],
        "message": '请发送图片'
    }
    return search_results


def reply_anime_group(eval_cqp_data):
    kaifuku = {
        "group_id": eval_cqp_data['group_id'],
        "message": "番剧截图识别中 请稍后......"
    }
    return kaifuku

def reply_anime(eval_cqp_data):
    kaifuku = {
        "user_id": eval_cqp_data['user_id'],
        "message": "番剧截图识别中 请稍后......"
    }
    return kaifuku

def reply_image(eval_cqp_data):
    kaifuku = {
        "user_id": eval_cqp_data['user_id'],
        "message": "图片搜索中 请稍后......"
    }
    return kaifuku

def reply_image_group(eval_cqp_data):
    kaifuku = {
        "group_id": eval_cqp_data['group_id'],
        "message": "图片搜索中 请稍后......"
    }
    return kaifuku