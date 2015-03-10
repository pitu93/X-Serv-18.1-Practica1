#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 contentApp class
 Simple web application for managing content

 Copyright Jesus M. Gonzalez-Barahona, Gregorio Robles 2009-2015
 jgb, grex @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - March 2015
"""

import webapp


class contentApp (webapp.webApp):
    """Simple web application for managing content.

    Content is stored in a dictionary, which is intialized
    with the web content."""

    # Declare and initialize content
    lista = []
    content = {}


    def imprim(self,lista):
        indice=0
        for elemento in lista:
            urls= ('url corta: ' + 'http://localhost:1234/' + str(indice) + ' url original: ' + elemento + '\n')
            indice+=1
            return urls
        return ''

    def parse(self, request):
        """Return the resource name (including /)"""
        metodo = request.split(' ',2)[0]
        recurso = request.split(' ',2)[1]
        if metodo == 'POST':
            cuerpo = request.split('\r\n\r\n',1)[1]
        elif metodo == 'GET':
            cuerpo = ''
        return(metodo,recurso,cuerpo)

    def process(self, resourceName):
        """Process the relevant elements of the request.

        Finds the HTML text corresponding to the resource name,
        ignoring requests for resources not in the dictionary.
        """
        formulario= "<form action='' method='POST'>Escribe una url: <input type='text' name='nombre' value='' /><br/><input type='submit'   value='Enviar' /></form>"
        #o se mete mal en la lista o se imprime mal
        if resourceName[0] == 'POST':
            if resourceName[1] == '/':
                url = str(resourceName[2]).split("=")[1] #error si no viene de formulario
                print 'URLLL' + url
                if url.startswith('http'):
                    url = 'http://' + url.split("%2F%2F", 2)[1]
                else:
                    url= 'http://' + url
                try:
                    corta= self.content[url] #hacerlo tambien si en el post va la acortada?
                    httpCode = "200 OK"
                    htmlBody = "<html><body>" + '<a href='+ url+ '>    larga   </a>' + '<a href= http://localhost:1234/'+ str(corta) + '>corta</a>' + formulario +'</body></html>'
                except KeyError:
                    self.lista.append(url)
                    self.content[url]=len(self.lista)-1
                    httpCode = "200 OK"
                    htmlBody = htmlBody = "<html><body>" + '<a href='+ url+ '>larga</a>' + '<a href= http://localhost:1234/'+ str(self.content[url]) + '>corta</a>' + formulario +'</body></html>'
                    
                
        elif resourceName[0] == 'GET':
            if resourceName[1] == '/':
                print self.imprim(self.lista)
                httpCode = "200 OK"
                htmlBody =  "<html><body>" + formulario +'<p>'+ self.imprim(self.lista) +'</p></body></html>'
            else:
                httpCode = "404 Not Found"
                htmlBody = "<html><body>Not Found" + formulario
        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
