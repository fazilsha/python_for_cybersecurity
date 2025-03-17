import argparse,validators,requests,yaml
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4 import Comment

parser = argparse.ArgumentParser(description="Web analyzer tool")
parser.add_argument("-v","--version",action="version",version='%(prog)s 1.0')
parser.add_argument("url",type=str, help="URL of the HTML to analyze")
parser.add_argument('--config', help="Path to configuration file")
parser.add_argument("-o","--output", help = "Report file output path")
args = parser.parse_args()
url=args.url

config = {'forms': True, 'comments': True, 'passwords': True}
 
if(args.config):
  print('Using config file: ' + args.config)
  config_file = open(args.config, 'r')
  config_from_file = yaml.load(config_file, Loader=yaml.FullLoader)
  if(config_from_file):
    config = { **config, **config_from_file}
    #config = config_from_file
    
report = ''

if validators.url(url):
    print("Getting the request for " + url)
    result_html = requests.get(url).text
    parsed_html = BeautifulSoup(result_html,'html.parser')
    # finding form tag
    forms=parsed_html.findAll('form')
    #finding Comments - Hardcoded keys
    comments = parsed_html.findAll(string=lambda text:isinstance(text, Comment))
    #Input validation
    password_inputs = parsed_html.findAll("input",{'name':'password'})
    if (config['forms']):
        for form in forms:
            if((form.get('action').find('https') < 0) and (urlparse(url).scheme != 'https')):
                is_form_secure = False
                report += "Form issue: Insecure form found:{0}\n".format(form.get('action'))
    if (config['comments']):
        for comment in comments:
            #print(comment.find('key: '))
            if comment.find('key: ') > -1:
                report += "Comment Issue: Key is found in the HTML \n"
    if (config['passwords']):
        for password_input in password_inputs:
            if password_input.find('type') != "password":
                report += "Input issue: Password captured in plainText found\n"
else:
    print("URL not valid, please provide full scheme")
    
if report == '':
    header = "Vulnerability Report for {0}:\n".format(url)
    header += "==========================================\n"
    report += "Awesome! Your HTML page is secure!!"
    report = header + report 
    print(report)
else:
    header = "Vulnerability Report for {0}:\n".format(url)
    header += "==========================================\n"
    report = header + report
    print(report)
    
if args.output:
    f = open(args.output, 'w')
    f.write(report)
    f.close()
    print("\n\nReport Saved to: " + args.output)