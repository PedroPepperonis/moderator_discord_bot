kick_request = {'member': 0}

print(kick_request)

kick_request.update({'member': +2})

kick_request.update({'member 2': 3})

for members in kick_request:
    if kick_request.get(members) == 3:
        print(f'{members} вы были кикнуты с сервера')

print(kick_request)