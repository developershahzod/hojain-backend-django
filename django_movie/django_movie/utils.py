# from movies.serializers import UserSerializer


def get_filename(filename, request):
    return filename.upper()

def my_jwt_response_handler(token, user=None, request=None):
    return {
        # 'token': token,
        # 'user': UserSerializer(user, context={'request': request}).data
    }