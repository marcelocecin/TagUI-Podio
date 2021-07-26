# tutorial serve apenas para quem utiliza o plano Premium do Podio, porque ele precisa do [Podio Workflow Automation](https://workflow-automation.podio.com) [PWA](https://help.podio.com/hc/en-us/sections/360005823819-Podio-Workflow-Automation) para fazer as automações
# this tutorial is only for those who use the Podio Premium plan, because it needs [Podio Workflow Automation](https://workflow-automation.podio.com) [PWA](https://help.podio.com/hc/en-us/sections/360005823819-Podio-Workflow-Automation) to do the automations

## este tutorial também utiliza script do [ProcFu](https://procfu.com) - [Onde o PWA não atende a todas as suas necessidades, Procfu e Quivvy Tools podem ajudar](https://help.podio.com/hc/en-us/articles/360019409639-Top-10-Best-Practices-for-Podio-Workflow-Automation)
## this tutorial also uses [ProcFu](https://procfu.com) script - [Where PWA doesn't meet all of your needs, Procfu and Quivvy Tools can help](https://help.podio.com/hc/en-us/articles/360019409639-Top-10-Best-Practices-for-Podio-Workflow-Automation)

### este exemplo utiliza certificado SSL emitido pela GoDaddy, mas você pode usar qualquer certificado, basta pesquisar na internet opções gratuitas de como emitir o seu
### this example uses SSL certificate issued by GoDaddy, but you can use any certificate, just search the internet for free options on how to issue yours

1. instalar o [TagUI](https://github.com/kelaberetiv/TagUI) (install [TagUI](https://github.com/kelaberetiv/TagUI))
2. utilizar o `app.py` para rodar a API - testado em servidor Linux Ubuntu (use `app.py` to run the API - tested on Ubuntu Linux server):
   - `celery -A python.app.celery worker --concurrency=1`
   - `celery -A python.app.celery flower`
   - `gunicorn -w 3 -b :5000 -t 30 --reload python.wsgi:app --certfile=ssl.crt --keyfile=ssl.key --ssl-version=TLS_SERVER`
3. [criar um aplicativo](https://help.podio.com/hc/en-us/articles/201019278-Creating-apps-) no Podio com um [campo Texto de várias linhas](https://help.podio.com/hc/en-us/articles/201019298-The-fields-in-app-templates) e com [ID único TAG com três campos decimais](https://help.podio.com/hc/en-us/articles/201019348-Adding-Unique-IDs-to-your-app-items) ([create an app](https://help.podio.com/hc/en-us/articles/201019278-Creating-apps-) on Podio with a [Multiline Text field](https://help.podio.com/hc/en-us/articles/201019298-The-fields-in-app-templates) and [unique ID TAG with three decimal fields](https://help.podio.com/hc/en-us/articles/201019348-Adding-Unique-IDs-to-your-app-items))
   - o campo em vermelho Nome não é necessário, utilizei ele apenas para facilitar a localização de quando há muitos scripts cadastrados (the field in red Name is not necessary, I used it just to make it easier to find when there are many registered scripts)
   - ao incluir o script no campo Texto de várias linhas, é muito importante que o texto seja pré-formatado, caso contrário a API não irá salvar o arquivo TAG no servidor na forma correta (when including the script in the Multiline Text field, it is very important that the text is preformatted, otherwise the API will not save the TAG file on the server in the correct way)
<img width="1189" alt="" src="https://user-images.githubusercontent.com/2955762/127058767-42afe9cf-8e7c-4662-81c7-6558e9de277b.png">
4. crie as automações dos flows no PWA de quando um item é criado e de quando um item é editado (create the flow automations in the PWA of when an item is created and when an item is edited)
<img width="309" alt="" src="https://user-images.githubusercontent.com/2955762/127059800-c5ae0fc5-7260-4de1-8e9a-f69c5b2d27dc.png">
<img width="737" alt="" src="https://user-images.githubusercontent.com/2955762/127059817-89f36ea3-8ea9-41a3-9ac4-0f51f42ae84c.png">
<img width="742" alt="" src="https://user-images.githubusercontent.com/2955762/127060161-f217eca2-0f5b-4aeb-86dd-6316b945e298.png">
5. crie uma última automação no PWA por data ou dia (create a last automation in PWA by date or day)
<img width="555" alt="" src="https://user-images.githubusercontent.com/2955762/127060840-dadf3ed6-7f3c-4197-961e-ab0e34505753.png">
<img width="746" alt="" src="https://user-images.githubusercontent.com/2955762/127061110-92868563-0a2a-40e6-968c-d41cc277eaa1.png">
6. dessa forma o script de exemplo básico será executado todos os dias no horário configurado (this way the basic example script will run every day at the configured time)
<img width="760" alt="" src="https://user-images.githubusercontent.com/2955762/127065498-7be87b77-1b7f-4e43-9a3e-d578f5f56efc.png">

### em breve irei atualizar esse tutorial para mostrar um exemplo de script e nova versão de API que anexa a imagem `top_result.png` no Podio
### I will soon update this tutorial to show an example script and new API version that attaches the `top_result.png` image to Podio
