from django.http import HttpResponseRedirect, JsonResponse



class processing_data:     
    def prueba1(data):
        msg = data['test']
        df= JsonResponse({'hello': msg}, safe= False)
        return df