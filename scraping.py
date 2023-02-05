import requests
from bs4 import BeautifulSoup


url = "https://www.siir-defteri.com/turk-sairler/"
path = "https://www.siir-defteri.com/"

 
def get_poet_url_main_page(url):
    links = []
    R = requests.get(url)
   
    soup = BeautifulSoup(R.text, "html.parser")
    #print(soup)
    
    sair = soup.find("div",{"class":"col-xs-12 col-sm-6"})
    
    for link in sair.find_all('a', href=True):
        #print(link['href'])
        links.append(link['href'])
        
    #anasayfada yer alan şairlerin linklerini döndürüyor
    # ornek -> /turk-sairler/A-Hicri-Izgoren/71
    return links


def full_url_poem(links):
    sair_link = []
    for link in links:
        new_path = path+link
        sair_link.append(new_path)
        #print(new_path)
    #get_poet_url_main_page 'in döndürdüğü linklerin başına ekleme 
    #yapar(yukarıdaki path).
    #ornek -> https://www.siir-defteri.com//turk-sairler/A-Hicri-Izgoren/71
    return sair_link

       
def get_poetry_urls(links):
    
    tum_siirler = []
    for link in links:
        R = requests.get(link)
        soup = BeautifulSoup(R.text, "html.parser")
        sair_url = soup.find("div",{"class":"pull-right bordered gradient padding hidden-on-mobile col-xs-12 col-sm-6 no-white-space"}).find("ul",{"class":"default-bullets"})
        #print(sair)

        for link in sair_url.find_all('a', href=True):
            print(path+link['href'])
            tum_siirler.append(path+link['href'])
            
    #Tum şairlerin şiirlerinin url'lerini döndürüyor
    return tum_siirler
        
                 
def get_poetry(links):
    
    poetry = open("poetry.txt", "w")
    for link in links:
        #print(link)
        R = requests.get(link)
        soup = BeautifulSoup(R.text, "html.parser")

        siirler = soup.find("div",{"class":"pull-right bordered gradient padding hidden-on-mobile col-xs-12 col-sm-6 no-white-space"}).text
        #print(siirler)
        sair_isimleri = soup.find("article").find("h4").text
        
        siir = soup.find("article").text.replace(siirler,"").replace(sair_isimleri,sair_isimleri+"\n \n")
        
        poetry.write(siir)
        
        #print(sair) 
        
        #print("\n")
    poetry.close()
       
def main():

    poem_links = get_poet_url_main_page(url)
    full_poem_links = full_url_poem(poem_links)
    poetry_urls = get_poetry_urls(full_poem_links)
    get_poetry(poetry_urls)
    

main()


