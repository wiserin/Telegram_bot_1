
# The class responsible for application data
class Data:

    # Method for working with a code word
    @staticmethod
    def code_word(state, **kwargs):
        if state == 'check':
            with open('app/app_data/text/code_word.txt', 'r') as file:
                text = file.read()
                if kwargs['code_word'] == text:
                    return True
                elif kwargs['code_word'] != text:
                    return False
        if state == 'change':
            with open('app/app_data/text/code_word.txt', 'w') as file:
                file.write(kwargs['text'])
                
    # Method for working with video
    @staticmethod
    def video(state, **kwargs):
        if state == 'read':
            with open(f'app/app_data/video/{kwargs["name"]}.txt', 'r') as file:
                token = file.read()
            return token
        if state == 'change':
            with open(f'app/app_data/video/{kwargs["name"]}.txt', 'w') as file:
                file.write(kwargs['video'])
        
