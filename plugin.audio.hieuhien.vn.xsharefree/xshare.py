# -*- coding: utf-8 -*-
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,urllib,urllib2,re,os,unicodedata,datetime,time,random,json

myaddon=xbmcaddon.Addon()
home=xbmc.translatePath(myaddon.getAddonInfo('path'));datapath=xbmc.translatePath(myaddon.getAddonInfo('profile'))
iconpath=os.path.join(datapath,'icon');datapath=os.path.join(datapath,'data')
datapath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'data'))
iconpath=xbmc.translatePath(os.path.join( xbmc.translatePath(myaddon.getAddonInfo('profile')),'icon'))
iconpath=xbmc.translatePath(os.path.join(home,"logos\\"))
iconpath=xbmc.translatePath(os.path.join(home,"logos"))
sys.path.append(os.path.join(home,'resources','lib'));from urlfetch import get,post
search_file=os.path.join(datapath,"search.xml");data_path=os.path.join(home,'resources','data')
try:rows=int(myaddon.getSetting('sodonghienthi'))
except:rows=30
tempfolder=xbmc.translatePath('special://temp');phim18=myaddon.getSetting('phim18')
xbmcplugin.setContent(int(sys.argv[1]), 'movies');homnay=datetime.date.today().strftime("%d/%m/%Y")
from resources.lib.utils import xsearch,xrw

media_ext=['aif','iff','m3u','m3u8','m4a','mid','mp3','mpa','ra','wav','wma','3g2','3gp','asf','asx','avi','flv','mov','mp4','mpg','mkv','m4v','rm','swf','vob','wmv','bin','cue','dmg','iso','mdf','toast','vcd','ts','flac','m2ts','dtshd','nrg'];icon={}
color={'vaphim':'[COLOR gold]','phimfshare':'[COLOR khaki]','4share':'[COLOR blue]','tenlua':'[COLOR fuchsia]','fptplay':'[COLOR orange]','trangtiep':'[COLOR lime]','search':'[COLOR lime]','ifile':'[COLOR blue]','hdvietnam':'[COLOR red]','hdviet':'[COLOR darkorange]','xshare':'[COLOR blue]','subscene':'[COLOR green]','chiasenhac':'[COLOR orange]','phimmoi':'[COLOR ghostwhite]','megabox':'[COLOR orangered]','hayhaytv':'[COLOR tomato]','kenh88':'[COLOR cyan]','phimdata':'[COLOR magenta]','phim47':'[COLOR springgreen]','phimsot':'[COLOR orangered]','hdonline':'[COLOR turquoise]','phim3s':'[COLOR lightgray]','kphim':'[COLOR lightgreen]','phimnhanh':'[COLOR chartreuse]','bilutv':'[COLOR hotpink]','anime47':'[COLOR deepskyblue]','phim14':'[COLOR chartreuse]','taifile':'[COLOR cyan]','phim':'[COLOR orange]','tvhay':'[COLOR gold]','nhacdj':'[COLOR fuchsia]','phimbathu':'[COLOR lightgray]','taiphimhd':'[COLOR blue]','hdsieunhanh':'[COLOR orangered]','nhaccuatui':'[COLOR turquoise]','imovies':'[COLOR orange]','vietsubhd':'[COLOR cyan]','imax':'[COLOR chartreuse]','mphim':'[COLOR deepskyblue]','vtvgo':'[COLOR green]'}
for hd in ['xshare','4share','downsub','favorite','fptplay','fshare','gsearch','hdvietnam','icon','id','ifiletv','ifile','isearch','khophim','maxspeed','megabox','movie','msearch','myfolder','myfshare','phimfshare','serverphimkhac','setting','tenlua','vaphim','hdviet','hayhaytv','chiasenhac','kenh88','phimdata','phim47','phimsot','hdonline','phim3s','kphim','phimnhanh','bilutv','anime47','phim14','taifile','phim','tvhay','nhacdj','phimbathu','taiphimhd','hdsieunhanh','phimmoi','nhaccuatui','imovies','vietsubhd','imax','mphim','vtvgo']:
	icon.setdefault(hd,os.path.join(iconpath,'%s.png'%hd))
hd={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/600.1.4 Gecko/20100101 Firefox/41.0'}

def mess(message='',title='',timeShown=5000):
	if not message:xbmc.executebuiltin("Dialog.Close(all, true)")
	else:
		title=': [COLOR blue]%s[/COLOR]'%title if title else ''
		s0='[COLOR green][B]Xshare[/B][/COLOR]'+title
		s1='[COLOR red]%s[/COLOR]'%message if '!' in message else u'[COLOR gold]%s[/COLOR]'%message
		xbmc.executebuiltin((u'XBMC.Notification(%s,%s,%s,%s)'%(s0,s1,timeShown,icon['icon'])).encode("utf-8"))

def mess_yesno(title='[COLOR green]Xshare[/COLOR]', line1='', line2='',no='No',yes='Yes'):
	dialog=xbmcgui.Dialog()#dialog.yesno(heading, line1[, line2, line3,nolabel,yeslabel])
	return dialog.yesno(title,line1,line2,nolabel=no,yeslabel=yes)

def no_accent(s):
	s=re.sub(u'??','D',s2u(s));s=re.sub(u'??','d',s)
	return unicodedata.normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def resolu(s):
	s=s.replace('HDG','').replace('HD','1080').replace('SD','640').replace('large','640').replace('medium','480').replace('small','360')
	result=xsearch('(\d+)',s)
	return result if result else '240'

def dl(l):#Direct link
	o=make_request(l,resp='o',maxr=5);h=''
	try:s=int(o.headers.get('content-length'))
	except:s=0
	s=0 if s<10**7 else s
	if s and o.history:h=o.history[-1].headers['location']
	elif s:h=l
	return h

def gdl(l,link=''):
	if type(l)==list:
		for href,label in l:
			link=dl(href)
			if link:break
	else:link=l
	return link

def s2u(s):return s.decode('utf-8') if isinstance(s,str) else s
def unescape(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s),s) for s in string.split())
def u2s(s):return s.encode('utf-8') if isinstance(s,unicode) else s
def printdict(mydict):print json.dumps(mydict,indent=2);return ''
def add_sep_item(label):addir_info('[COLOR lime]--%s--[/COLOR]'%label,'',icon['xshare'],'',100,1,'')
def labelsearch(label):return '%s%s[/COLOR]'%(color['search'],label)
def namecolor(name,c=''):return '[COLOR %s]%s[/COLOR]'%(c,name) if c else re.sub('\[[^\[]+?\]','',name)

def open_category(query): #category.xml
	if query=='MMN':root=True
	else:root=False
	pattern='<a server="(.+?)" category="(.+?)" mode="(\d+)" color="(.*?)" icon="(.*?)">(.+?)</a>'
	items=re.findall(pattern,makerequest(joinpath(data_path,'category.xml')));q='';fanart=home+'/fanart.jpg'
	for server,category,mode,colo,icon,name in items:
		if (server!=query) or (("18" in category) and (myaddon.getSetting('phim18')=="false")):continue
		if query=='VPH' and mode!='10':q='vaphim.xml'
		elif query=='IFI' and mode!='10':q='ifiletv.xml'
		else:q=category
		name='[COLOR '+colo+']'+name+'[/COLOR]';icon=joinpath(iconpath,icon)
		addir(name,category,icon,fanart,mode=int(mode),page=0,query=q,isFolder=(mode!='16'),root=root)
	if q=='vaphim.xml':
		body=makerequest(joinpath(datapath,"vp_menu.txt"));icon=joinpath(iconpath,'vaphim.png')
		if not body:mess(u'??ang update menu...','vaphim.com');return#vp_make_datanew();return
		for query,name in eval(body):
			if "18" in name and myaddon.getSetting('phim18')=="false":continue
			addir('%s%s[/COLOR]'%(color['vaphim'],name),'vaphim.xml',icon,fanart,92,1,query,True,root=root)
	#if query=='MMN' and (myaddon.getSetting('my_nas_url')!="http://buffalonas.com/"):
	#	addir('[COLOR lime]My NAS[/COLOR]','',os.path.join(iconpath,'csn.png'),fanart,52,1,'home',True,root=root)

def servers_list(name,url,img,fanart,mode,page,query):
	def make_ls(s):
		i=0;l=len(s)
		for d,m in s:#sl:server location
			title=namecolor('Kho phim tr??n %s'%d,color[d.split('.')[0]].replace('[COLOR ','').replace(']',''));i+=1
			if i==1:menu={'servers_list':{'action':'Down'}}
			elif i<l:menu={'servers_list':{'action':'Up-Down'}}
			else:menu={'servers_list':{'action':'Up'}}
			addir_info(title,d,joinpath(iconpath,d.split('.')[0]+'.png'),'',int(m),1,d,True,menu=menu)
	
	from resources.lib.servers import servers_list;srv=servers_list()
	menu={'servers_list':{'action':'Up-Down'}}
	if query=='FRE':
		s=srv.mylist();l=len(s)
	#	for i in range(l/10+(1 if l%10>0 else 0)):
	#		addir_info(namecolor('Servers group %d'%(i+1),'lime'),str(i),icon['xshare'],'',mode,1,'group',True)
		
	#	add_sep_item('All servers ------------------------------------------------')
		make_ls(s)
	
	elif query=='group':
		s=srv.mylist();i=0;l=len(s)
		def mm(i):return i+10 if i+10<len(s) else i+len(s)%10
		make_ls([[s[i] for i in range(i,mm(i))] for i in range(0,len(s),10)][int(url)])
			
	
	else :step=-1 if query=='Up' else 1;srv.move(url,step);xbmc.executebuiltin("Container.Refresh")

def clean_string(string):
	return ' '.join(s for s in re.sub('Fshare|4share|Tenlua','',string).split())

def remove_tag(string):
	if '::' in string:string=string.split('::')[1]
	string=re.sub('\t|\n|\r|\f|\v|vn|Fshare|fshare|4share|4Share|TenLua|tenlua|List xml',' ',string)
	string=re.sub('\[/?COLOR.*?\]|\[\s*\]|\(.*?\)|\{.*?\}|<.*?>|\"|\'|-|\||,|&\w*;|/|br|\.',' ',string)
	return ' '.join(i for i in u2s(unescape(string)).split())

def joinpath(p1,p2):
	try:p=os.path.join(p1,p2)
	except:p=os.path.join(p1,s2u(p2))
	return p

def init_file():
	datafolder=xbmc.translatePath(myaddon.getAddonInfo('profile'))
	for folder in (datafolder,datapath,iconpath,myfolder,tempfolder,subsfolder,xsharefolder):
		if not os.path.exists(folder):os.mkdir(folder)
	xmlheader='<?xml version="1.0" encoding="utf-8">\n';p=datapath;q=myfolder
	for i in [(p,'search.xml'),(p,'hdvietnam.xml'),(p,'favourites.xml'),(p,'phimmoi.xml'),(p,'fpt.xml'),(q,'mylist.xml')]:
		file=joinpath(i[0],i[1])
		if not os.path.isfile(file):makerequest(file,xmlheader,'w')

def sub_body(content,s1,s2):
	if not isinstance(content,str):content=str(content)
	if s1 and s2:result=content[content.find(s1):content.find(s2)]
	elif s1:result=content[content.find(s1):]
	elif s2:result=content[:content.find(s2)]
	else:result=content
	return result

def json_rw(file,dicts={},key=''):
	if dicts:makerequest(joinpath(datapath,file),json.dumps(dicts),'w')
	else:
		try:dicts=json.loads(makerequest(joinpath(datapath,file)))
		except:dicts={}
		if key:dicts=dicts.get(key,())
	return dicts

def get_dict(dict,key_list=list(),result=''):
	for key in key_list:
		dict=dict.get(key,result)
		if dict==result:break
	return dict

def sets(lists):
	temp=list()
	for s in lists:
		if s not in temp:temp.append(s)
	return temp

def folders(folder,result=list()):#get files fullpath from folder and subfolders
	for f in os.listdir(folder):
		f=joinpath(folder,f)
		if os.path.isdir(f):folders(f,result)
		else:result.append(f)
	return result

def delete_files(folder,mark=''):
	temp='ok'
	for file in os.listdir(folder):
		if os.path.isfile(joinpath(folder,file)) and (not mark or mark in file):
			try:os.remove(joinpath(folder,file))
			except:temp='';pass
	return temp

def delete_folder(folder):
	for file in os.listdir(folder):
		try:
			files=joinpath(folder,file)
			if os.path.isdir(files):delete_folder(files);os.rmdir(files)
			#for f in os.listdir(files):
			#	os.remove(joinpath(files,f))
			else:os.remove(files)
		except:pass

def rename_file(sf,df,kq='ok'):
	try:
		if os.path.isfile(df):os.remove(df)
		os.rename(sf,df)
	except:kq='';pass
	return kq

def endxbmc():
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def xbmcsetResolvedUrl(url,name='',img=''):
	if img:item=xbmcgui.ListItem(path=url, iconImage=img, thumbnailImage=img)
	else:item=xbmcgui.ListItem(path=url)
	if 'Maxlink' in name:
		if name!='Maxlink':name=name.replace('Maxlink','');item.setInfo('video', {'Title':name})
		else:item.setInfo('video', {'Title':os.path.basename(url)})
		name=''
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item);endxbmc()
	if myaddon.getSetting('autoload_sub')=='true' and name!='xshare':
		if name:url=name
		urltitle=urllib.unquote(os.path.splitext(os.path.basename(url))[0]).lower()
		urltitle='.'+'.'.join(s for s in re.sub('_|\W+',' ',re.split('\d\d\d\d',urltitle)[0]).split())+'.'
		subfile='';items=[]
		for file in os.listdir(subsfolder):
			filefullpath=joinpath(subsfolder,file).encode('utf-8')
			filename=re.sub('vie\.|eng\.','',os.path.splitext(file)[0].lower().encode('utf-8'))
			filename=re.split('\d\d\d\d',filename)[0];count=0
			for word in re.sub('_|\W+',' ',filename).split():
				if '.%s.'%word in urltitle:count+=1
			if count:items.append((count,filefullpath))
		for item in items:
			if item[0]>=count:count=item[0];subfile=item[1]
		if subfile:
			xbmc.sleep(2000);xbmc.Player().setSubtitles(subfile)
			mess(u'%s'%s2u(os.path.basename(subfile)),'Auto load sub',5000)

def addir(name,link,img='',fanart='',mode=0,page=0,query='',isFolder=False,root=False):
	def xquote(href):return urllib.quote_plus(href)
	if '18+' in name and phim18=="false":return
	name=unescape(re.sub(',|\|.*\||\||\<.*\>','',u2s(name)))
	item=xbmcgui.ListItem(name,iconImage=img,thumbnailImage=img)

	if not root:
		label='[COLOR lime]Add to My Favourites V2[/COLOR]'
		q='Add-'+(query.split('?')[1] if '?' in query else query)+'-'+('F' if isFolder else '')
		cmd='RunPlugin(plugin://%s/?'%myaddon.getAddonInfo('id');items=list()
		cmd=cmd+'&name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s)'
		cmd=cmd%(xquote(name),xquote(url),xquote(img),xquote(fanart),100+mode,page,xquote(q))
		command=[(label,cmd)]
	else:command=[]
	
	query=menuContext(name,link,img,fanart,mode,query,item,command)
	item.setInfo(type="Video", infoLabels={"title":name})
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	item.setProperty('Fanart_Image',fanart)
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s'
	li=li%(sys.argv[0],xquote(name),xquote(link),xquote(img),xquote(fanart),mode,page,xquote(query))
	if not isFolder:item.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

def addirs(name,href,img='',fanart='',query=''):
	name=clean_string(name)
	if not fanart and iconpath not in img:fanart=img
	if 'xml' in query:
		if name=='mylist.xml':name=color['subscene']+name+'[/COLOR]'
		query=query.replace('xml','');name='%sList xml[/COLOR]-%s'%(color['fptplay'],name)
		addir(name,href,img,fanart,mode=97,query=query,isFolder=True)
	elif query=='file':addir(name,href,img=icon['icon'],mode=96,query=query,isFolder=True)
	elif 'www.fshare.vn/file' in href:
		if 'ph??? ????? vi???t' in u2s(name).lower():
			name=color['fshare']+'Ph??? ????? Vi???t[/COLOR]-%s'%name
			addir(name,href,img,fanart,mode=3,query=query,isFolder=True)
		else:addir(color['fshare']+'Fshare[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'www.fshare.vn/folder' in href:
		if s2u('chia s???') in s2u(name):name=color['trangtiep']+name+'[/COLOR]'
		else:name=color['fshare']+name+'[/COLOR]'
		addir(name,href,img,fanart,mode=90,query=query,isFolder=True)
	elif '4share.vn/d/' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif '4share.vn' in href:
		addir(color['4share']+'4share[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'tenlua.vn/fm/folder/' in href or '#download' in href:
		addir(color['tenlua']+name+'[/COLOR]',href,img,fanart,mode=95,query=query,isFolder=True)
	elif 'tenlua.vn' in href:
		addir(color['tenlua']+'TenLua[/COLOR]-%s'%name,href,img,fanart,mode=3,query=query)
	elif 'subscene.com' in href:
		addir(color['subscene']+'Subscene[/COLOR]-%s'%name,href,img,fanart,mode=94,query='download',isFolder=True)
	elif 'http://pubvn.' in href:
		addir(color['4share']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)
	elif 'http://vuahd.tv' in href:
		addir(color['vuahd']+name+'[/COLOR]',href,img,fanart,mode=38,query=query,isFolder=True)

def menuContext(name,link,img,fanart,mode,query,item,command=[]):
	if query.split('?')[0]=='Search':
		query=query.split('?')[1]
		command+=searchContext(name,link,img,fanart,mode)
	elif query.split('?')[0]=='ID':
		query=query.split('?')[1]
		command+=searchContext(name,link,img,fanart,15)
		command+=favouritesContext(name,link,img,fanart,mode)
	elif 'fshare.vn' in link or '4share.vn' in link or 'tenlua.vn' in link:#mode in (3,38,90,95):
		command+=favouritesContext(name,link,img,fanart,mode)
	elif myfolder in s2u(link):
		command+=make_myFile(name,link,img,fanart,mode,query)
	elif query in 'hdvietfolder-hdvietplay':
		command+=hdvietContext(name,link,img,fanart,mode)
	item.addContextMenuItems(command)
	return query

def makeContext(name,link,img,fanart,mode,query):
	if query=='Add to MyFshare favorite':make='AddFavorite'
	elif query=='Remove from MyFshare favorite':make='RemoveFavorite'
	elif query=='Remove All':make='Remove All'
	else:make=query.split()[0]
	if 'Rename' in make:colo=color['fshare']
	elif 'Remove' in make:colo=color['hdvietnam']
	else:colo=color['trangtiep']
	context=colo+query+'[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link,img,fanart,make)
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	return context,cmd

def hdvietContext(name,link,img,fanart,mode):
	context=color['trangtiep']+'Th??m v??o phim y??u th??ch[/COLOR]'
	p=(myaddon.getAddonInfo('id'),mode,name,link.split('_')[0],img,fanart,'Themmucyeuthich')
	cmd='RunPlugin(plugin://%s/?mode=%d&name=%s&url=%s&img=%s&fanart=%s&query=%s)'%(p)
	command=[(context,cmd)]
	return command

def searchContext(name,link,img,fanart,mode):
	command=[(makeContext(name,link,img,fanart,9,'Rename item'))]
	command.append((makeContext(name,link,img,fanart,9,'Remove item')))
	command.append((makeContext(name,link,img,fanart,9,'Remove All')))
	return command

def favouritesContext(name,link,img,fanart,mode):
	def makecmd(mode,title):command.append((makeContext(name,link,img,fanart,mode,title)))
	command=[];link=u2s(link)
	if link in makerequest(joinpath(datapath,"favourites.xml")):	
		makecmd(98,'Rename in MyFavourites');makecmd(98,'Remove from MyFavourites')
	else:makecmd(98,'Add to MyFavourites')
	if 'www.fshare.vn' in link:
		if query=='MyFshare':makecmd(11,'Remove from MyFshare');makecmd(11,'Rename from MyFshare')
		else:makecmd(11,'Add to MyFshare')
		if query=='favorite':makecmd(11,'Remove from MyFshare favorite')
		else:makecmd(11,'Add to MyFshare favorite')
	if link in makerequest(joinpath(myfolder,'mylist.xml')):
		makecmd(12,'Rename in Mylist.xml');makecmd(12,'Remove from Mylist.xml')
	else:makecmd(12,'Add to Mylist.xml')
	command.append((makeContext(name,'addstring.xshare.vn',img,fanart,13,'Add item name to string search')))
	return command

def make_myFile(name,link,img,fanart,mode,query):
	name=re.sub('\[/?COLOR.*?\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip();command=[]
	if os.path.isfile(s2u(link)):
		command.append((makeContext(name,link,img,fanart,11,'Upload to MyFshare')));temp='file'
	else:temp='folder'
	command.append((makeContext(name,link,img,fanart,96,'Rename this %s'%temp)))
	command.append((makeContext(name,link,img,fanart,96,'Remove this %s'%temp)))
	return command

def make_mySearch(name,url,img,fanart,mode,query):
	body=makerequest(search_file)
	if query=='Rename':
		label=' '.join(s for s in name.split())
		string=get_input('Nh???p chu???i m???i',re.sub('\[.*\]-','',label)).strip()
		if not string or string==label:return
		string=' '.join(s for s in string.split())
		if re.search('http.?://',url):
			content=re.sub('<a href="%s">.+?</a>\n'%url,'<a href="%s">%s</a>\n'%(url,string),body)
		else:content=body.replace(name,string)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'S???a 1 m???c th??nh c??ng');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		name=re.sub('\(|\)|\[|\]|\{|\}|\?|\,|\+|\*','.',name)
		content=re.sub('<a href="%s">.+?</a>\n|<a>%s</a>\n'%(url,name),'',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'X??a 1 m???c th??nh c??ng');xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove All':
		content=re.sub('<a href=".+?">.+?</a>\n','',body)
		if body!=content:
			makerequest(search_file,content,'w')
			mess(u'X??a t???t c??? c??c m???c th??nh c??ng');xbmc.executebuiltin("Container.Refresh")
	elif query=='Add':
		if url and not re.search(url,body):makerequest(search_file,'<a href="%s">%s</a>\n'%(url,name),'a')
	elif query=='Input':
		query = get_input('Nh???p chu???i t??n phim c???n t??m tr??n %s'%url);attr='a'
		if query:
			query = ' '.join(s for s in query.replace('"',"'").replace('?','').split() if s!='')
			if query not in body:
				makerequest(search_file,'<a>%s</a>\n'%query,'a');xbmc.executebuiltin("Container.Refresh")
		else:query=''
	elif query=='get':
		srv=url.split('.')[0];site='Google ' if mode==2 else ''
		if url=='chiasenhac.com':
			menu={'MyPlaylist':{'action':'Search','server':['chiasenhac.com']}}
			name='%s%sSearch[/COLOR] tr??n %s%s[/COLOR] Nh???p chu???i t??m ki???m m???i - '+myaddon.getSetting('csn_s')
			name=name%(color['search'],site,color[srv],url)
			addir_info(name,url,icon[srv],'',mode,1,'INP',True,menu=menu)
		else:
			name='%s%sSearch[/COLOR] tr??n %s%s[/COLOR] Nh???p chu???i t??m ki???m m???i'
			name=name%(color['search'],site,color[srv],url)
			addir_info(name,url,icon[srv],'',mode,1,'INP',True)
		menu={'MySearch':{'action':'Add','server':['xshare.vn']}}
		if myaddon.getSetting('history')=='true':
			for s in re.findall('<a>(.+?)</a>',body):addir_info(s,url,icon[srv],'',mode,4,s,True,menu=menu)
	return query

def make_myFshare(name,url,img,fanart,mode,query):#11
	def nameClean(s):
		return ' '.join(re.sub('\[/?COLOR.*?\]|\\\|/|:|\*|\?|\<|\>|\!|,|\@|\"|--|\.\.|\#|\$|\%|\^|\|','',s).split())
	
	myFshare=myaddon.getSetting('thumucrieng')
	from resources.lib.servers import fshare
	if query=='Add':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		name=nameClean(name);fs.myFshare_add(url,name);xbmc.sleep(1000)
	elif query=='Rename':
		fs=fshare();old_name=new_name='';
		new_name=get_input('S???a t??n 1 m???c trong MyFshare',nameClean(name)).strip();new_name=nameClean(new_name)
		if not new_name or new_name==old_name:return
		else:new_name=url.split('/')[4].strip()+('FOLDER ' if 'folder' in url else 'FILE ')+new_name
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.myFshare_rename(url,new_name):xbmc.executebuiltin("Container.Refresh")
	elif query=='Remove':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.myFshare_remove(url):xbmc.executebuiltin("Container.Refresh")
	elif query=='Upload':
		try:
			size=os.path.getsize(s2u(url));name=re.sub('\[/?COLOR.*?\]','',os.path.basename(url)).strip()
			if size>10*1024**2:mess(u'Add-on ch??a h??? tr??? upload file>10MB!','myFshare');return
			f=open(s2u(url),'rb');content=f.read();f.close()
		except:mess(u'File read error','Fshare.vn');return
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		fs.myFshare_upload(name,size,content)
	elif query=='AddFavorite':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		fs.Favorite_add(url)
	elif query=='RemoveFavorite':
		fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'),myFshare)
		if fs.Favorite_remove(os.path.basename(url)):xbmc.executebuiltin("Container.Refresh")
	if fs.logged:fs.logout()
	return

def make_favourites(name,url,img,fanart,mode,query):
	favourites=joinpath(datapath,"favourites.xml");name=remove_tag(name)
	if query=='Add':
		if url.strip() in makerequest(favourites):mess(u'M???c n??y ???? c?? trong MyFavourites!','MyFavourites');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(favourites,string,'a'):mess(u'???? th??m 1 m???c v??o MyFavourites','MyFavourites')
		else:mess(u'Th??m 1 m???c v??o MyFavourites th???t b???i!','MyFavourites')
	elif query=='Rename':
		title = get_input('S???a t??n trong m???c MyFavourites',name).strip()
		if not title or title==name:return 'no'
		body=makerequest(favourites)
		string=re.search('((<a href="%s" img=".*?" fanart=".*?">).+?</a>)'%(url),body)
		if string:
			body=body.replace(string.group(1),string.group(2)+title+'</a>')
			if makerequest(favourites,body,'w'):
				mess(u'???? s???a 1 m???c trong MyFavourites','MyFavourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'S???a 1 m???c trong MyFavourites th???t b???i!','MyFavourites')
		else:mess(u'S???a 1 m???c trong MyFavourites th???t b???i!','MyFavourites')
	elif query=='Remove':
		body=makerequest(favourites);string=xsearch('(<a href="%s" img=".*?" fanart=".*?">.+?</a>)'%url,body)
		if string:
			body=body.replace(string+'\n','')
			if makerequest(favourites,body,'w'):
				mess(u'???? x??a 1 m???c trong xshare favourites','MyFavourites')
				xbmc.executebuiltin("Container.Refresh")
			else:mess(u'X??a 1 m???c trong xshare favourites th???t b???i!','MyFavourites')
		else:mess(u'X??a 1 m???c trong xshare favourites th???t b???i!','MyFavourites')
	else:
		items=re.findall('<a href="(.+?)" img="(.*?)" fanart="(.*?)">(.+?)</a>',makerequest(favourites))
		for href,img,fanart,name in items:addirs(name,href,img,fanart)
	return

def make_mylist(name,url,img,fanart,mode,query):
	mylist=joinpath(myfolder,'mylist.xml')
	name=re.sub('\[COLOR.{,12}\]|\[/COLOR\]|Fshare|4share|TenLua|List xml|-|:|"','',name).strip()
	if query=='Add':
		if url.strip() in makerequest(mylist):mess(u'M???c n??y ???? c?? trong MyList!','MyList');return
		if img==fanart:fanart=''
		string='<a href="%s" img="%s" fanart="%s">%s</a>\n'%(url.strip(),img,fanart,name)
		if makerequest(mylist,string,'a'):mess(u'???? th??m 1 m???c v??o mylist.xml','MyList')
		else:mess(u'Th??m v??o mylist.xml th???t b???i!','MyList')
	elif query=='Rename':
		title = get_input('S???a t??n 1 m???c trong mylist.xml',name)
		if not title or title==name:return 'no'
		string1='<a href="%s" img=".*?" fanart=".*?">.+?</a>'%url
		string2='<a href="%s" img=".*?" fanart=".*?">%s</a>'%(url,title)
		body=re.sub(string1,string2,makerequest(mylist))
		if makerequest(mylist,body,'w'):
			mess(u'???? s???a 1 m???c trong mylist.xml','MyList');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'S???a 1 m???c trong mylist.xml th???t b???i!','MyList')
	elif query=='Remove':
		string='<a href="%s" img=".*?" fanart=".*?">.+?</a>\n'%url
		body=re.sub(string,'',makerequest(mylist))
		if makerequest(mylist,body,'w'):
			mess(u'???? x??a 1 m???c trong mylist.xml','MyList');xbmc.executebuiltin("Container.Refresh")
		else:mess(u'X??a 1 m???c trong mylist.xml th???t b???i!','MyList')
	return

def make_request(url,headers=hd,resp='b',maxr=0):
	try:
		if maxr==0:response=get(url,headers=headers)#,timeout=2)
		else:response=get(url,headers=headers,max_redirects=maxr)#,timeout=2)
		if resp=='o':resp=response
		else:
			if resp=='j':resp=response.json
			elif resp=='s':resp=response.status
			elif resp=='u':resp=response.text
			elif resp=='c':resp=response.cookiestring
			else:resp=response.body
			response.close()
	except:
		if resp=='j':resp=dict()
		elif resp=='s':resp=500
		else:resp=''
		if 'vaphim.com' not in url:
			link=xsearch('//(.{5,20}\.\w{2,3})',s2u(url))
			if not link:link=url
			mess(u'L???i k???t n???i t???i: %s!'%xsearch('//(.{5,20}\.\w{2,3})',s2u(url)),'make_request')
		print 'L???i k???t n???i t???i: %s!'%u2s(url);
	return resp#unicode:body=response.text

def make_post(url,headers=hd,data='',resp='o'):
	try:
		if data:response=post(url=url,headers=headers,data=data,timeout=10)
		else:response=post(url=url,headers=headers,timeout=10)
		if resp=='b':response=response.body
		elif resp=='j':response=response.json
	except:
		mess(u'Post link error: %s!'%s2u(url),'make_post');print 'Post link error: %s'%u2s(url)
		response={} if resp=='j' else ''
	return response

def xread(url,hd={'User-Agent':'Mozilla/5.0'},data=None):
	req=urllib2.Request(url,data,hd)
	try:res=urllib2.urlopen(req, timeout=20);b=res.read();res.close()
	except:b=''
	return b

def makerequest(file,body='',attr='r'):
	file=s2u(file)
	if attr=='r':
		try:f=open(file);body=f.read();f.close()
		except:body=''
	else:
		try:f=open(file,attr);f.write(body);f.close()
		except:mess(u'L???i ghi file: %s!'%s2u(os.path.basename(file)),'makerequest');body=''
	return body

def get_input(title=u"", default=u""):
	result = ''
	keyboard = xbmc.Keyboard(default, title)
	keyboard.doModal()
	if keyboard.isConfirmed():result = keyboard.getText().strip()
	else:result = ''
	return result

def tenlua_get_detail_and_starting(id,headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	data='[{"a":"filemanager_builddownload_getinfo","n":"%s","r":0}]'%id
	response=make_post('https://api2.tenlua.vn/',headers,data,resp='j')
	try:json=response[0]
	except:json={'type':'none'}
	return json

def resolve_url(url,xml=False):
	urltemp=url.lower()
	if 'fshare.vn' in urltemp:result=fshare_resolve('https://www.%s'%xsearch('(fshare.vn.+?)\Z',url),xml)
	elif '4share.vn' in urltemp:result=fourshare_resolve(url)
	elif 'tenlua.vn' in urltemp:result=tenlua_resolve(url,xml)
	return result

def fshare_resolve(url,xml):
	from resources.lib.servers import fshare
	fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
	if fs.logged is None:return 'fail'
	for loop in range(6):
		if loop>0:mess(u'Get link l???n th??? %d'%(loop+1),'fshare.vn');xbmc.sleep(sleep);sleep+=1000
		direct_link=fs.get_maxlink(url)
		if direct_link=='fail':break
		elif direct_link:break
	fs.logout()
	if not direct_link:mess('Sorry! Potay.com','fshare.vn');return 'fail'
	elif direct_link in 'notfound-fail':return 'fail'
	elif xml:return direct_link
	else:return xshare_resolve(direct_link,os.path.splitext(direct_link)[1][1:].lower())

def fourshare_resolve(url):
	hd['Cookie']=login4share()
	if not hd['Cookie']:return 'fail'#login fail
	response=xread(url,hd);logout_site(hd['Cookie'],url)
	if not response:xbmc.sleep(2000);return 'fail'
	direct_link=xsearch("<a style='text-decoration:none' href='(.+?)'>",response)
	if not direct_link:
		direct_link=xsearch("Link Download.+?href='(.+?4share.vn.+?)'>",response)
		if not direct_link:
			direct_link=xsearch("'http.+\?info=.+)'",response)
			if not direct_link:
				mess(u'Kh??ng get ???????c maxspeed link!','resolve_url');return 'fail'
	ext=os.path.splitext(xsearch('<title>(.+?)</title>',response))[1][1:].lower()
	return xshare_resolve(direct_link,ext)

def fourshare_resolve1(url):
	hd['Cookie']=login4share()
	if not hd['Cookie']:return 'fail'#login fail
	response=make_request(url,hd,resp='o');logout_site(hd['Cookie'],url)
	if not response or response.status!=200:xbmc.sleep(2000);return 'fail'
	direct_link=xsearch("<a style='text-decoration:none' href='(.+?)'>",response.body)
	if not direct_link:
		direct_link=xsearch("Link Download.+?href='(.+?4share.vn.+?)'>",response.body)
		if not direct_link:
			direct_link=xsearch("'http.+\?info=.+)'",response.body)
			if not direct_link:
				mess(u'Kh??ng get ???????c maxspeed link!','resolve_url');return 'fail'
	ext=os.path.splitext(xsearch('<title>(.+?)</title>',response.body))[1][1:].lower()
	return xshare_resolve(direct_link,ext)

def tenlua_resolve(url,xml):
	hd['Cookie']=logintenlua();id=xsearch('\w{14,20}',url,0);direct_link=''
	if not id:id=url.split('/download/')[1].split('/')[0]
	download_info=tenlua_get_detail_and_starting(id,hd);print download_info
	filename=u2s(download_info.get('n',''))
	ext=os.path.splitext(filename)[1][1:].lower()
	size=int(download_info.get('real_size','0'))
	dlink=download_info.get('dlink','')
	if not dlink:
		dlink=download_info.get('url','');mess(u'Slowly direct link!','resolve_url')
		if not dlink:mess(u'Kh??ng get ???????c max speed link!','resolve_url');return 'fail'
	response=make_request(dlink,hd,resp='o');logout_site(hd['Cookie'],url)
	if response and response.status==302:return xshare_resolve(response.headers['location'],ext)
	else:mess(u'Kh??ng get ???????c max speed link!','resolve_url');return 'fail'

def xshare_resolve(direct_link,ext='',filmlabel=''):
	def get_detail_maxlink(direct_link):
		response=make_request(direct_link,{'User-Agent':'xshare'},resp='o')
		if not response:return 'fail'
		detail=response.headers
		size=int(detail.get('content-length',0))
		filename=detail.get('content-disposition','').split('=')
		if len(filename)>1:filename=filename[1].replace('"','').replace("'","")
		else:filename=os.path.basename(direct_link)
		ext=os.path.splitext(filename)[1][1:].lower()
		return response,size,filename,ext
	
	if ext in media_ext:xbmcsetResolvedUrl(direct_link,filmlabel);return ''
	#elif ext in ['srt','sub','txt','smi','ssa','ass','nfo']:xbmcsetResolvedUrl(direct_link,filmlabel);return ''
	
	response,size,filename,ext=get_detail_maxlink(direct_link)
	if ext in 'xml':result=doc_list_xml(direct_link,'list_xml')
	elif ext in media_ext or filmlabel:xbmcsetResolvedUrl(direct_link,filmlabel);result=''
	elif ext in ['rar','zip','srt','sub','txt','smi','ssa','ass','nfo']:
		result=xshare_download(response,size,filename,ext)
	elif not ext:mess('sorry! this is not a media file','Check media extention');result='fail'
	else:xbmcsetResolvedUrl(direct_link);result=''
	#mess('sorry! this is not a media file','xshare resolve');result='fail'
	return result

def xshare_download(response,size,filename,ext):
	def checkmedia(file):
		return os.path.isfile(file) and os.path.getsize(file)>1024**2 and os.path.splitext(file)[1][1:] in media_ext
	
	temp_path=joinpath(tempfolder,'temp');mediafile=False
	if not os.path.exists(temp_path):os.mkdir(temp_path)
	else:delete_folder(temp_path)
	tempfile=joinpath(temp_path,'tempfile.%s'%ext)
	
	if size<1024**2:#sub file
		if myaddon.getSetting('autodel_sub')=='true':delete_folder(subsfolder)
		content=makerequest(tempfile,response.body,"wb")
	elif size<2*1024**3:
		if size>1024**3:size_str='%d.%d GB'%(size/(1024**3),(size%(1024**3))/10**7)
		else:size_str='%d.%d MB'%(size/(1024**2),(size%(1024**2))/10**4)
		line1='[COLOR green]File: %s - %s[/COLOR]'%(filename,size_str)
		line2='S??? m???t nhi???u th???i gian t???i file v??o "[B]Th?? M???c C???c B???[/B]"!';content=''
		if size<100*1024**2 or  mess_yesno('xshare c???nh b??o',line1,line2,'No - Kh??ng t???i','Yes - ?????ng ?? t???i'):
			losslessfolder=joinpath(myfolder,'Lossless')
			if not os.path.exists(losslessfolder):os.mkdir(losslessfolder)
			if size>100*1024**2:endxbmc()
			f=open(tempfile,'wb');i=0;mess(u'Started Background download...',timeShown=50000);i=j=t=0;fn=''
			for chunk in response:
				f.write(chunk);i+=len(chunk)
				if i*10/size>j:j+=1;mess(u'???? download ???????c %d%%'%(j*10),timeShown=20000)
			f.close();mess(u'??ang Unzip...',timeShown=10000)
			xbmc.sleep(1000);xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,u2s(losslessfolder)),True)
			for filefullpath in folders(losslessfolder):
				if not checkmedia(filefullpath) and 'nrg' not in filefullpath:os.remove(filefullpath)
				elif os.path.getmtime(filefullpath)>t:fn=filefullpath;t=os.path.getmtime(fn)
			if fn and size<100*1024**2:#File nh???, g???i play
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=fn))
			mess(u'???? download xong. H??y m??? Th?? M???c C???c B??? v?? th?????ng th???c ti???p nh??',timeShown=20000)
	else:mess(u'Sorry! Dung l?????ng file qu?? l???n. Ch??a x??? l??');content=''
	if not content:return 'no'
	sub_ext = [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"];sub_list=[];p=',|"|\''
	if content[0] in 'R-P':
		xbmc.sleep(1000);xbmc.executebuiltin('XBMC.Extract("%s")'%tempfile,True)
		for filefullpath in folders(temp_path):
			file=os.path.basename(filefullpath)
			if os.path.isfile(filefullpath) and os.path.splitext(filefullpath)[1] in sub_ext:
				if re.search('english|eng\.|\.eng',filename.lower()) and myaddon.getSetting('autotrans_sub')=='true':
					mess(u'Google ??ang d???ch sub t??? ti???ng Anh sang ti???ng Vi???t','Subs Downloader',timeShown=20000)
					filetemp=xshare_trans(filefullpath,filefullpath)
					if rename_file(filetemp,joinpath(subsfolder,'Vie.%s'%re.sub(p,'',file))):
						mess(u'???? d???ch xong sub t??? ti???ng Anh sang ti???ng Vi???t','Subs Downloader')
					elif rename_file(filefullpath,joinpath(subsfolder,'Eng.%s'%re.sub(p,'',file))):
						mess(u'Kh??ng d???ch ???????c sub. Gi??? nguy??n b???n ti???ng Anh!','Subs Downloader') 
				elif re.search('english|eng\.|\.eng',filename.lower()) and rename_file(filefullpath,joinpath(subsfolder,'Eng.%s'%re.sub(p,'',file))):
					mess(u'???? download sub v??o Subsfolder','Subs Downloader') 
				elif re.search('vietnam|vie\.|\.vie',filename.lower()) and rename_file(filefullpath,joinpath(subsfolder,'Vie.%s'%re.sub(p,'',file))):
					mess(u'???? download sub v??o Subsfolder','Subs Downloader') 
				elif rename_file(filefullpath,joinpath(subsfolder,re.sub(',|"|\'','',file))):
					mess(u'???? download sub v??o Subsfolder','Subs Downloader') 
	elif rename_file(tempfile,joinpath(subsfolder,'Vie.%s'%filename)):
		mess(u'???? download sub v??o Subsfolder','Subs Downloader')
	return 'no'

def xshare_trans(fs,fd):
	def trans(s):
		try:s=s.decode('unicode_escape') if '\\' in s else s.decode('utf-8')
		except:pass
		return s

	f=open(fs);b=f.read();f.close();s='';S=''
	u='https://translate.googleapis.com/translate_a/single?ie=UTF-8&oe=UTF-8&client=gtx&sl=en&tl=vi&dt=t&q=%s'
	list_1=b.splitlines();list_2=[];rows=len(list_1);row=0
	hd={'Referer':'https://translate.google.com/','User-Agent':'Mozilla/5.0 (Windows NT 6.3) Chrome/49.0.2623.112 Safari/537.36','Cookie':''}
	for i in list_1:
		row+=1
		if re.search('[a-zA-Z]',i):s=s+' '+i+' xshare';list_2.append('xshare')
		else:list_2.append(i.strip())
		if len(s)>1000 or row==rows:
			mess(u'Google ???? d???ch %d %%'%(row*100/rows), timeShown=1500)
			s=' '.join(i for i in s.split())
			tran=make_request(u%urllib.quote(s),headers=hd,resp='o')
			if not hd['Cookie']:hd['Cookie']=tran.cookiestring
			xbmc.sleep(1000)#;print tran.body
			try:
				l=eval(tran.body.replace(',,,',',').replace(',,"en"',''))
				S=S+' '.join(i[0] for i in l[0])
			except:xbmc.executebuiltin("Dialog.Close(all, true)");return ''
			s=''
	s=' '.join(trans(i) for i in S.split())
	list_3=s.split('xshare');d=0;f=open(fd,'w')
	f.write('0\n00:00:00,000 --> 00:01:30,000\n[COLOR gold]Xshare dich Anh-->Viet bang Google translate[/COLOR]\n\n')
	for i in list_2:
		try:
			if i=='xshare':f.write(list_3[d].strip().encode('utf-8')+'\n');d+=1
			else:f.write(i+'\n')
		except:pass
	f.close();xbmc.executebuiltin("Dialog.Close(all, true)")
	return fd

def logout_site(cookie,url):
	def logout(cookie,url,site):
		hd['Cookie']=cookie
		mess(u'Logout %s %sth??nh c??ng'%(site,'' if make_request(url,hd,resp='s')==302 else u'kh??ng '))
	if cookie and myaddon.getSetting('logoutf')=="true":
		if 'fshare.vn' in url.lower():logout(cookie,'https://www.fshare.vn/logout','Fshare.vn')
		elif '4share.vn' in url.lower():logout(cookie,'http://4share.vn/default/index/logout','4share.vn')
		elif 'dangcaphd.com' in url.lower():logout(cookie,'http://dangcaphd.com/logout.html','dangcaphd.com')
		elif 'tenlua.vn' in url.lower():logouttenlua(cookie)

def loginfshare(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	response=make_request("https://www.fshare.vn/login",resp='o');result=''
	if not response:mess(u'L???i k???t n???i Fshare.vn!','fshare.vn');return result
	fs_csrf=xsearch('value="(.+?)".*name="fs_csrf',response.body);headers['Cookie']=response.cookiestring
	username=myaddon.getSetting('usernamef');password=myaddon.getSetting('passwordf')
	form_fields = {"LoginForm[email]":username,"LoginForm[password]":password,"fs_csrf":fs_csrf}
	response=make_post("https://www.fshare.vn/login",headers,form_fields)
	if response.status==302:mess(u'Login th??nh c??ng','Fshare.vn');result=response.cookiestring
	else:mess(u'Login kh??ng th??nh c??ng!','Fshare.vn')
	return result

def login4share(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	form_fields = {"username":myaddon.getSetting('username4'),"password":myaddon.getSetting('password4')}
	response=make_post('http://up.4share.vn/index/login',headers,form_fields)
	if response and response.status==302:mess(u'Login th??nh c??ng','4share.vn');f=response.cookiestring
	else:mess(u'Login kh??ng th??nh c??ng!','4share.vn');f=''
	return f

def logintenlua(headers={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
	user=myaddon.getSetting('usernamet');pw=myaddon.getSetting('passwordt')
	data='[{"a":"user_login","user":"'+user+'","password":"'+pw+'","permanent":"true"}]'
	response=make_post('https://api2.tenlua.vn/',headers,data)
	if response and response.body!='[-1]':mess(u'Login th??nh c??ng','tenlua.vn');f=response.headers.get('set-cookie')
	else:mess(u'Login kh??ng th??nh c??ng!','tenlua.vn');f=''
	return f

def logouttenlua(cookie):
	hd['Cookie']=cookie
	response=make_post('https://api2.tenlua.vn/',hd,'a=user_logout')
	if response:mess(u'Logout th??nh c??ng','tenlua.vn')
	else:mess(u'Logout kh??ng th??nh c??ng!','tenlua.vn')

def hdvn_boss_room(url,body):
	if re.search('-\d{1,3}\.html',url):
		body=xread(re.sub('-\d{1,3}\.html','.html',url))
	pattern='id="postcount\d{5,8}" name="1">.{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?).html"'
	return xsearch(pattern,body,1,re.DOTALL)

def hdvn_body_thanked(body,hd,bossroom):
	sec_token= xsearch('name="securitytoken" value="(.{50,60})"',body)
	home='http://www.hdvietnam.com/diendan/';thanks_data=[];content=''
	pattern='id="postcount(\d{5,8})".{,1000}line popupctrl.{40,55}/\d{4,10}-(.+?)\.html'
	items=re.findall(pattern,body,re.DOTALL);dataremove='do=post_thanks_remove_user&using_ajax=1'
	if not items:return''
	for id_post,name in items:
		if name==bossroom:
			data='do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(id_post,sec_token)
			make_post(home+'post_thanks.php',hd,data)
			data='do=whatever&p=%s&all=%s&securitytoken=%s'%(id_post,id_post,sec_token)
			content+=make_post(home+'showthread.php',hd,data).body
			if not re.search('return post_thanks_remove_user.%s'%id_post,body):
				thanks_data.append('%s&p=%s&securitytoken=%s'%(dataremove,id_post,sec_token))
	for data in thanks_data:make_post(home+'post_thanks.php',hd,data)
	return content

def google_ifile(url,name,temp=[]):
	if 'http://ifile.tv/phim/' not in url:return temp
	mess(url)
	for url4share,fanart,name2,catalog in ifile_tv_4share(url):
		if not name2:name2=name
		if url4share not in temp:temp.append(url4share);addirs(name2,url4share,fanart,fanart)
	mess()
	return temp

def google_vaphim(url,temp=[]):
	if url=='http://vaphim.com/':return temp
	elif '/tag/' in url:
		pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
		url=xsearch(pattern,xread(url))
		if not url:return temp
	mess(url)
	for id,title,href,img,fanart,category in vp_2fshare(url):
		if href not in temp:temp.append(href);addirs(title,href,img,fanart)
	mess()
	return temp

def search_get_page(name,url,img,fanart,mode,page,query):
	if 'vaphim.com/' in url:
		if url=='http://vaphim.com/':return
		elif '/tag/' in url:
			pattern='class="entry-title"><a href="(.+?)" rel="bookmark"'
			url=xsearch(pattern,xread(url))
			if not url:return
		for id,title,href,img,fanart,category in vp_2fshare(url):
			addir_info(title,href,img,fanart)
	if '4share.vn/' in url.lower():
		for href,img,title,category in ifile_tv_4share(url):
			addir_info(title,href,img,fanart)
	if 'ifile.tv/' in url.lower():
		if 'http://ifile.tv/phim/' not in url:return 
		for url4share,fanart,name2,catalog in ifile_tv_4share(url):
			if not name2:name2=name
			addir_info(name2,url4share,fanart,fanart)

def google_search_api(url,start,string,items):#url:fshare.vn,4share.vn,tenlua.vn,hdvietnam.com
	string_search = urllib.quote_plus('"%s"'%string)
	href = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&'
	href+='start=%s&q=site:%s+%s'%(start,url.lower(),string_search)
	try:j=json.loads(xread(href))
	except:j=dict()
	#json=make_request(href,resp='j')
	if not j:return items,'end'
	if j.get('responseStatus')!=200 and myaddon.getSetting('googlesearch')=='API':
		mess(u'Google: nghi ng??? l???m d???ng D???ch v???. T??? ?????ng chuy???n sang web search!','google_search_api')
		return google_search_web(url,start+'xshare',string,items)
	data=j.get('responseData',dict())
	if not data.get('results'):return items,'end'
	currentPage=int(data['cursor']['currentPageIndex'])+1;nextPage=0
	for item in data['results']:
		name=remove_tag(item['titleNoFormatting'])
		if len(name.split())<2:name=os.path.basename(item['url'])
		if 'tenlua' in url and not re.search('\w{14,20}/(.*)\Z',item['url']):continue
		elif not name or 'Forum' in name or 'server-nuoc-ngoai' in item['url']:continue
		elif 'chuyenlink.php' in item['url']:continue
		items.append((name,urllib.unquote(item['url'].encode('utf-8'))))
	start=str(int(start)+8)
	if start not in [s['start'] for s in data['cursor']['pages']]:start='end'
	return items,start

def google_search(url,query,mode,page,items=[]):
	srv=url.split('.')[0]
	if page==0:make_mySearch('',url,'','',mode,'get');return
	elif page==1:
		query=make_mySearch('',url,'','','','Input');page=2
		if query is None or not query.strip():return 'no'
	query=no_accent(query)
	if '?' in query:start=query.split('?')[1];query=query.split('?')[0]
	else:start='0'
	if myaddon.getSetting('googlesearch')=='Web' or 'xshare' in start:items,start=google_search_web(url,start,query,items)
	else:items,start=google_search_api(url,start,query,items)
	if len(items)<10 and start!='end' and myaddon.getSetting('googlesearch')=='API':
		return google_search(url,'%s?%s'%(query,start),mode,page,items)
	if not items and start=='end':mess(u'Kh??ng t??m th???y d??? li???u y??u c???u!','google_search');return 'no'
	for name,link in set(items):
		if url=='hdvietnam.com':addir_info(name,link,icon[srv],query='get_link_post')
		elif url=='vaphim.com':
			if '/tag/' not in link:addir_info(name,link,icon[srv],query='vp_getsubpage')
		else:addir_info(name,link,icon[srv])
	if start!='end':
		name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%str(page-2)
		addir_info(name,url,icon[srv],'',mode,page+1,'%s?%s'%(query,start),True)
	return ''

def google_search_web(url,start,query,items):
	num='30';google = 'https://www.google.com.vn/search?hl=vi&ie=utf-8&oe=utf-8&num=%s&'%num
	#num='30';google = 'https://www.google.com.vn/search?hl=vi&num=%s&'%num
	string_search = urllib.quote_plus('"%s"'%query);srv=url.split('.')[0]
	if 'xshare' in start:start=start.replace('xshare','');xshare='yes'
	else:xshare=''
	href=google+'start=%s&q=site:%s+%s'%(start,url.lower(),string_search);print href
	
	hd['Cookie']=makerequest(joinpath(xsharefolder,'google.cookie'))
	cookie=urllib2.HTTPCookieProcessor();opener=urllib2.build_opener(cookie);urllib2.install_opener(opener)
	body=xread(href,hd)
	cookie=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
	if checkupdate('google.cookie',hours=240,folder=xsharefolder) and cookie:
		makerequest(joinpath(xsharefolder,'google.cookie'),cookie,'w')

	if '<TITLE>302 Moved</TITLE>' in body and myaddon.getSetting('googlesearch')=='Web':
		mess(u'Google: nghi ng??? l???m d???ng D???ch v???. T??? ?????ng chuy???n sang API search!','google_search_web')
		return google_search_api(url,start,query,items)

	if url=='fshare.vn':
		links=re.findall('<h3 class="r"><a href="(http.?://www.fshare.vn/.+?)".+?>(.+?)</a>',body)
		for link,name in links:
			items.append((remove_tag(unescape(name)),link.replace('http:','https:')))
	elif url=='vaphim.com':
		links=re.findall('<h3 class="r"><a href="(http://vaphim.com/.+?)".+?>(.+?)</a>',body)
		for link,name in links:
			items.append((remove_tag(unescape(name)),link.replace('http:','https:')))
	else:
		links=re.findall('<a href=".*?(http.+?)["|&].+?>(.+?)</a></h3>',body)
		for link,name in links:
			if 'tenlua.vn' in link and not re.search('\w{14,20}/(.*)\Z',link):continue
			elif not name or 'Forum' in name or 'server-nuoc-ngoai' in link:continue
			elif 'chuyenlink.php' in link:continue
			items.append((remove_tag(unescape(name)),link))
	start=str(int(start)+int(num))
	if 'start=%s'%start not in body:start='end'
	elif 'xshare':start=start+'xshare'
	return items,start

def main_menu(category,page,mode,query): #Doc list tu vaphim.xml hoac ifiletv.xml
	items = doc_xml(joinpath(datapath,query),para=category);pages=len(items)/rows+1
	del items[0:page*rows];count=0;down=len(items)
	for id,img,fanart,href,name in items:
		down-=1;addirs(name,href,img,fanart);count+=1
		if count>rows and down>10:break
	if down>10:
		page+=1;name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,category,icon['icon'],mode=mode,page=page,query=query,isFolder=True)

def update_xml(items_new,items_old,filename): #update vaphim,ifiletv xml
	try:items = sorted(items_new+items_old,key=lambda l:int(l[1]),reverse=True)
	except:items = items_new+items_old
	contents='<?xml version="1.0" encoding="utf-8">\n'
	for id_tip,id_htm,category,img,fanart,href,fullname in items:
		content='<a id_tip="%s" id="%s" category="%s" img="%s" fanart="%s" href="%s">%s</a>\n'
		content=content%(id_tip,id_htm,category,img,fanart,href,fullname);contents+=content
	if makerequest(joinpath(datapath,filename),contents,'w'):
		mess(u'???? c???p nh???t ???????c %d phim'%len(items_new),'%s Auto update'%filename)
	else: mess(u'???? x???y ra l???i c???p nh???t!','%s Auto update'%filename)
	return

def vp_page(url,body=''):#id,name,href,img,category
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	pattern='<li class="post-(\d{4,6})(.+?)">.+?src="(.+?)".+?<h3 class="entry-title">'
	pattern+='<a href="(.+?)" rel="bookmark" >(.+?)</a>';items=[]
	if not body:body=xread(url,hd)
	for id,category,img,href,name in re.findall(pattern,body,re.DOTALL):
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if [s for s in ['game','video-clip','phn-mm','ebooks'] if s in category]:continue
		name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name).split())
		items.append((id,name,href,img,category))
	return items

def vp_2fshare(url):#id,title,href,img,fanart,category
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	body=xread(url,hd)
	if not body:
		body=xread(url,hd)
		if not body:return list()
	
	items=list();id=xsearch("href='http://vaphim.com/\?p=(.+?)'",body)
	temp=xsearch('<div id=".+?" class="post-(.+?)">',body)
	category=' '.join(s.replace('category-','') for s in temp.split() if 'category-' in s)
	if not id or [s for s in category.split() if s in 'game video-clip phn-mm ebooks']:return items
	temp=xsearch('<title>(.+?)</title>',body)
	name=' '.join(s for s in re.sub('<.+?>|&.+?; ?|\||VaPhim.com','',temp).split())
	image=xsearch('meta property="og:image" content="(.+?)"',body)
	pattern='<a \w{4,6}=".*?(fshare.vn/f.l.?e?r?/.+?|http://subscene.+?)".{,18}>(.+?)</a><'
	if 'collection' not in category:
		content=xsearch('id="attachment_(.+?)"cf5_wpts_cl"',body,1,re.DOTALL)
		if not name:
			temp=xsearch('class="wp-caption-text">(.+?)<',content)
			name=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',temp).split())
		temp=re.findall('src="(.+?\.jpg|.+?\.png).{,10}"',content)
		img=temp[0] if len(temp)>0 else image;fanart=temp[1] if len(temp)>1 else ''
		for href,title in re.findall(pattern,content):
			if '//' in title:title=''
			title=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',title).split() if s not in name)
			title='.'.join(s for s in title.split('.') if s not in name)
			title=name+' '+title;href=href.replace('fshare.vn','https://www.fshare.vn')
			items.append((id,title,href,img,fanart,category))
	else:
		body=body[body.find('"content"'):]
		links=re.findall(pattern,body)
		if body.find('"text-align: center;"')>0:begin='"text-align: center;"' 
		elif body.find('<p><strong>')>0:begin='<p><strong>'
		elif body.find('id="attachment_')>0:begin='id="attachment_'
		elif body.find('"wordpress-post-tabs"')>0:begin='"wordpress-post-tabs"'
		else:begin='"section"'
		for content in re.findall('(%s.+?"cf5_wpts_cl")'%begin,body,re.DOTALL):
			temp=re.findall('src="(.+?\.jpg|.+?\.png).{,10}"',content)
			img=temp[0] if len(temp)>0 else image;fanart=temp[1] if len(temp)>1 else ''
			title=xsearch('<strong>(.+?)</strong>(</span></p>|</p>|<br />)',content)
			if not title:title=xsearch('"wp-caption-text">(.+?)<',content)
			title=name+' '.join(s for s in re.sub('<.+?>|&.+?; ?','',title).split() if s not in name)
			for href,fn in re.findall(pattern,content):
				fn=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',fn).split() if s not in title)
				fn='.'.join(s for s in fn.split('.') if s not in title)
				fn=title+' '+fn;href=href.replace('fshare.vn','https://www.fshare.vn')
				items.append((id,fn,href,img,fanart,category))
		if len(items)<len(links):
			temp='-'.join(os.path.basename(s[2]) for s in items)
			for href,fn in links:
				if os.path.basename(href) in temp:continue
				if '//' in fn:fn=''
				fn=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',fn).split() if s not in name)
				fn='.'.join(s for s in fn.split('.') if s not in name)
				fn=name+' '+fn;href=href.replace('fshare.vn','https://www.fshare.vn')
				items.append((id,fn,href,image,fanart,category))
	return items

def vp_update(auto=True):#vp_2fshare(url):id,title,href,img,fanart,category
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');time_vp_update=my_dict.get('vp_update_time','0')
	if int(timenow)-int(time_vp_update)<1 and auto:return 'no'
	else:my_dict['vp_update_time']=timenow;my_dict=my_dict=json_rw('xshare.json',my_dict)
	items=vp_page('http://vaphim.com/category/phim-2/');hrefs=[];items_new=[]
	if not items:return 'no'
	ids=my_dict.get('vp_update_ids',list());mess(u'Vaphim updating ...',homnay)
	my_dict['vp_update_ids']=[s[0] for s in items];my_dict=json_rw('xshare.json',my_dict)
	items_old=doc_xml(joinpath(datapath,"vaphim.xml"));href_old=[s[5] for s in items_old]
	if auto:#update all in phim-2 page
		for href in [s[2] for s in items]:hrefs+=vp_2fshare(href)
	else:
		for href in [s[2] for s in items if s[0] not in ids]:
			mess('Vaphim updating...','vaphim.com');hrefs+=vp_2fshare(href)
	for id,title,href,img,fanart,category in [s for s in hrefs if s[2] not in href_old]:
		items_new.append(('',id,category,img,fanart,href,title))
	if items_new:update_xml(items_new,items_old,"vaphim.xml")
	else:mess(u'Kh??ng c?? phim m???i...','Vaphim.com auto update')
	return 'ok'

def vp_list(name,url,img,mode,page,query):#92 query='phim-le'
	if url=='folder':
		items=list(set([s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if s[1]==query]))
		for id_tip,id,category,img,fanart,href,name in items:addirs(name,href,img,fanart)
	elif url in 'vaphim.xml-collection':
		if url=='collection':query=url;url='vaphim.xml';page=1
		items=list(set([s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if query in s[2]]))
		ids=list(set([s[1] for s in items]));ids.sort(reverse=True);pages=len(ids)/rows+1
		del ids[:(page-1)*rows];down=len(ids);del ids[rows:]
		for id in ids:vp_addir([s for s in items if s[1]==id])
		if down>rows:
			name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
			addir(name,url,icon['icon'],mode=mode,page=page+1,query=query,isFolder=True)

def vp_addir(items):
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimfshare'],name)
	if not items:return
	elif len(items)==1:
		for id_tip,id,category,img,fanart,href,name in items:addirs(name,href,img,fanart)
	else:
		id_tip,id,category,img,fanart,href,name=items[0]
		name='[COLOR goldenrod]'+subtitle_of_year(name).replace('(','')+'[/COLOR]'
		addir(name,'folder',img,fanart,92,1,id,True)
	
def vp_phimmoi():
	txtfile=joinpath(datapath,'vp_phimmoi.txt')
	if not os.path.isfile(txtfile):return
	ids=eval(makerequest(txtfile))
	items=[s for s in doc_xml(joinpath(datapath,'vaphim.xml')) if s[1] in ids]
	for id in ids:vp_addir([s for s in items if s[1]==id])

def vp_xemnhieu():
	txtfile=joinpath(datapath,'vp_xemnhieu.txt')
	if not os.path.isfile(txtfile):return
	names=eval(makerequest(txtfile))
	items=doc_xml(joinpath(datapath,'vaphim.xml'));i=0
	for name in names:vp_addir([s for s in items if name in s[6]])

def vp_chonloc():
	txtfile=joinpath(datapath,'vp_chonloc.txt')
	if not os.path.isfile(txtfile):return
	names=eval(makerequest(txtfile))
	items_xml=doc_xml(joinpath(datapath,"vaphim.xml"));ids=[s[1] for s in items_xml]
	for name in names:
		name=name.split('<br/>');nv=' '.join(s for s in re.sub('<.+?>|&.+?; ?','',name[0]).split())
		if len(name)<2:vp_addir([s for s in items_xml if nv in s[6]])
		else:ne=' '.join(s for s in name[1].split());vp_addir([s for s in items_xml if nv in s[6] or ne in s[6]])

def vp_make_datanew():
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	body=xread('http://vaphim.com/huong-dan-lay-rss-cua-vaphim-com/',hd)
	names=re.findall('<li><a href=".+?" title=".+?">(.+?)<',body)
	if names:makerequest(joinpath(datapath,'vp_xemnhieu.txt'),str(names),'w')
	items=re.findall('<li><a href="/category.+?/([\w-]+?)/">(.+?)</a></li>',body)
	if items:makerequest(joinpath(datapath,"vp_menu.txt"),str(items),'w')
	body=xread('http://vaphim.com/',hd)
	items=re.findall('"post-(\d{4,6})(.+?)"',body);items_new=[]
	for id,category in items:
		category=' '.join(s.replace('category-','') for s in category.split() if 'category-' in s)
		if not any(s for s in category.split() if s in 'game video-clip phn-mm ebooks'):items_new.append(id)
	if items_new:makerequest(joinpath(datapath,'vp_phimmoi.txt'),str(items_new),'w')
	items=re.findall('rel="bookmark">(.+?)</a>',body)
	if items:makerequest(joinpath(datapath,"vp_chonloc.txt"),str(items),'w')

def daklak47(name,url,img):
	reps = make_request(url)
	if reps.status==302:
		req=reps.headers['location']
		url = req.replace('http:','https:')
		if 'www.fshare.vn/folder/' in url:mess(u"Ch??a x??? l?? tr?????ng h???p ?????c folder tr??n 47daklak.com");return
		else:resolve_url(url)
	else: mess(u'Kh??ng t??m th???y link tr??n %s!'%s2u(url),'47daklak.com')

def ifile_home(name,url,img,mode,page,query):
	pattern='href=".+(\d{5}).+" class="mosaic-backdrop"'
	
	if url=="search":make_mySearch('','ifile.tv','','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return ifile_home(name,'ifile.tv',img,mode,page,query)
		else:return 'no'
	elif url=="ifile.tv":
		search_string = urllib.quote_plus(query)
		url='http://ifile.tv/search?search_string=%22'+urllib.quote_plus(query)+'%22&search_module=phim&time_sort=new'
		body=make_request(url,headers=hd)
		for img,href,title in re.findall("src='(.+?)'.+?href='(.+?)'>([^<]+?)</a></b>",body):
			if 'http://ifile.tv' not in href:href='http://ifile.tv'+href
			if 'http://ifile.tv' not in img:img='http://ifile.tv'+img
			title=' '.join(s for s in title.split())
			addir_info(title,href,img,'',mode,1,'film',True)
			
	elif url=="demo" or query=="demo":#ifile de nghi
		url='http://ifile.tv/phim/index' if url=="demo" else url
		body=make_request(url,headers=hd)
		for s in re.findall('("box-widget-grid fl-box".+?"film_tooltip")',body,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			if 'http://ifile.tv' not in href:href='http://ifile.tv'+href
			img=xsearch('src="(.+?)"',s)
			if 'http://ifile.tv' not in img:img='http://ifile.tv'+img
			title=xsearch("<a href='.+?'>(.+?)</a>",s).replace('<br>','').replace('<br/>','')
			title=' '.join(s for s in title.split())
			addir_info(title,href,img,'',mode,1,'film',True)
		return
		pattern='a href=".+(\d{5})\.htm">.*\s.*\s.*<img src=".+?" title=".+?"';query="demo"
	elif query=="film":
		body=make_request(url,headers=hd)
		
		for href,size in re.findall("link_down.+?href='([^<]+?)'>.+?<b>([^/]+?)</b>",body):
			title=name+' - '+size.strip();addirs(title,href,img,'')
		subs=xsearch("<b>Subtitle:</b>.+?href='([^<]+?)'>",body)
		if subs:addirs(name,subs,img,'')
		
		add_sep_item('----------Phim C??ng th??? lo???i---------')
		for s in re.findall('(left_news_div_table.+?news_tooltip)',body,re.DOTALL):
			href=xsearch("<a href='(.+?)'>",s)
			if 'http://ifile.tv' not in href:href='http://ifile.tv'+href
			img=xsearch("src=.?'(.+?)'",s)
			if 'http://ifile.tv' not in img:img='http://ifile.tv'+img
			title=xsearch("<a href='.+?'>(.+?)</a>",s).replace('<br>','').replace('<br/>','')
			title=' '.join(s for s in title.split())
			addir_info(title,href,img,'',mode,1,'film',True)
			
	elif url=="index" or query=="index":#xem nhieu
		hd['Referer']='http://ifile.tv/phim/page/1' if url=="index" else url
		response=make_post('http://ifile.tv/phim/index/filter/type/special_filter',hd,'type=special_filter&filter_by_view_desc=1')
		hd['Cookie']=response.cookiestring;query='index';hd['Referer']=='http://ifile.tv/phim/index'
		url='http://ifile.tv/phim' if url=="index" else url
	elif url=="new":url='http://ifile.tv/phim'#Moi nhat
	body=make_request(url,headers=hd)
	id_new='-'.join(s for s in re.findall(pattern,body))
	for id_tip,id,category,img,fanart,href,name in doc_xml(joinpath(datapath,"ifiletv.xml")):
		if id in id_new:addirs(name,href,img,fanart)
	url=xsearch('<a href="(.+?)" title="Next"',body)
	if url and query!="demo":
		page=xsearch('/(\d{1,3})',url);trangcuoi=xsearch('<a href=".+?/(\d{1,3})" title="End"',body)
		name=color['trangtiep']+'Trang ti???p theo: trang %s/%s[/COLOR]'%(page,trangcuoi)
		addir(name,'http://ifile.tv%s'%url,img,fanart,mode,int(page),query,True)
		
def doc_list_xml(url,filename='',page=1):
	if page<2:
		items=doc_xml(url,filename=filename);page=1
		makerequest(joinpath(tempfolder,'temp.txt'),str(items),'w')
	else:f=open(joinpath(tempfolder,'temp.txt'));items=eval(f.readlines()[0]);f.close()
	pages=len(items)/rows+1
	del items[0:(page-1)*rows];count=0
	for id,href,img,fanart,name in items:
		if '47daklak.com' in href: addir(name,href,img,mode=47)
		else: addirs(name,href,img,fanart)
		count+=1
		if count>rows and len(items)>(rows+10):break
	if len(items)>(rows+10):
		name=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,pages)
		addir(name,url,iconpath+'khophim.png','',97,page+1,'',isFolder=True)

def doc_xml(url,filename='',para=''): 
	if (datapath in url) or (myfolder in s2u(url)):body=makerequest(url)
	elif filename=='list_xml':body=make_request(url)
	else:body=make_request(resolve_url(url,xml=True))

	if ('vaphim' in url) or ('ifiletv' in url) or ('phimfshare' in url) or ('hdvietnam' in url):
		if para and para[:6]=='search':
			string=para[7:].replace('(','.').replace(')','.')
			if ('phimfshare' in url) or ('hdvietnam' in url):
				r='href="(.+?)" img="(.+?)">(.*%s.*)</a>'%string
				items=[(s[1],s[1],s[0],s[2]) for s in re.findall(r,no_accent(body),re.IGNORECASE)]
			else:
				r='img="(.*?)" fanart="(.*?)" href="(.+?)">(.*%s.*)</a>'%string
				items=re.compile(r, re.I).findall(no_accent(body))
		else:
			if not para:r='<a id_tip="(.*?)" id="(.+?)" category="(.*?)" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'
			else: #Doc theo category
				r='<a.*id="(.+?)" category=".*%s.*" img="(.*?)" fanart="(.*?)" href="(.+?)">(.+?)</a>'%para
			items = sorted(re.findall(r,body),key=lambda l:l[0], reverse=True)
	else:#Doc cac list xml khac
		r='<a.+id="(.*?)".+href="(.+?)".+img="(.*?)".+fanart="(.*?)".*>(.+?)</a>'
		items = re.compile(r).findall(body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".+img="(.*?)".*()>(.+?)</a>',body)
		if len(items)<1:items = re.findall('.+()href="(.+?)".*()()>(.+?)</a>',body)
		if (myaddon.getSetting('copyxml')=="true") and ('http' in url) and (len(items)>0) :
			filename=re.sub('\.xml.*','.xml',filename.replace('[COLOR orange]List xml[/COLOR]-',''))
			filename=re.sub('\[.{1,10}\]','',filename);f_fullpath=joinpath(myfolder,filename)
			if not os.path.isfile(f_fullpath):
				string='<?xml version="1.0" encoding="utf-8">\n'
				for id,href,img,fanart,name in items:
					string+='<a id="%s" href="%s" img="%s" fanart="%s">%s</a>\n'%(id,href,img,fanart,name)
				if makerequest(f_fullpath,string,'w'):
					mess(u'???? t???i file %s v??o MyFolder'%s2u(filename))
	return items

def fshare_page_file(url):
	body = make_request(url)
	name=clean_string(xsearch('<title>(.+?)</title>',body))
	if not name or 'L???i 404' in name:mess(u'Kh??ng t??m th???y n???i dung qu?? kh??ch y??u c???u!','fshare.vn');return 'no'
	size=xsearch('<i class="fa fa-hdd-o"></i>(.+?)</div>',body).strip()
	return name+' - '+size

def doc_TrangFshare(name,url,img,fanart,query=''):
	from resources.lib.servers import fshare
	if 'favorite' in url:fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
	else:fs=fshare()
	folder_detail=fs.get_folder(url)
	for title,href,iD,size,date in sorted(folder_detail.get('items'), key=lambda k: k[0]):
		if 'file' in href and len(size)>3:title+=' - size:%s'%size
		addirs(title,href,img,fanart,query+'xml' if '.xml' in title.lower() else query)
	if fs.logged:fs.logout()
	return folder_detail['pagename']

def doc_Trang4share(url,temp=[]):#38
	if '4share.vn/d/' in url:
		response=xread(url)
		if '[Empty Folder]' in response:mess('Folder is empty','4share.vn');return temp
		pattern="<a href='(.+?)' target='.+?'><image src = '.+?'>(.+?)<.*?><td style='text-align: right'>(.+?)</td>"
		pattern+="|<a href='(.+?)'>.*\s.*<image src = '.+?'>(.+?)</a></div>"
		for href,name,size,folder_link,folder_name in re.findall(pattern,response):
			if href:name=name.strip()+' - '+size.strip();href='http://4share.vn'+href
			else:href='http://4share.vn'+folder_link;name=folder_name.strip()
			if href not in temp:temp.append((href));addirs(name,href)
	elif '4share.vn/f/' in url:
		name_size=re.search('Filename:.{,10}>(.+?)</strong>.{,20}>(.+?)</strong>',make_request(url))
		if name_size:
			name=name_size.group(1)+' - '+name_size.group(2)
			if url not in temp:temp.append((url));addirs(name,url)
	return temp

def doc_thumuccucbo(name,url,img,fanart,mode,query):
	if url=='thumuccucbo':url=myfolder
	url=s2u(url)
	if query=='Remove':
		if os.path.isfile(url):
			try:os.remove(url);mess(u'???? x??a file: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			except:mess(u'L???i x??a file!','MyFolder')
		else:
			import shutil
			try:shutil.rmtree(url);mess(u'???? x??a th?? m???c: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			except:mess(u'L???i x??a th?? m???c!','MyFolder')
	elif query=='Rename':
		name=s2u(os.path.basename(url))
		name_new = get_input('xshare - Rename file/folder (ch?? ?? ph???n m??? r???ng)',name)
		if name_new and name_new!=name:
			if rename_file(url,joinpath(os.path.dirname(url),name_new)):
				mess(u'???? ?????i t??n file/folder: %s'%s2u(url),'MyFolder');xbmc.executebuiltin("Container.Refresh")
			else:mess(u'L???i Rename file/folder!','MyFolder')
	elif myfolder in url and query!='file':
		for filename in os.listdir(url):
			filenamefullpath = u2s(joinpath(url, filename));filename= u2s(filename)
			size=os.path.getsize(joinpath(url, filename))/1024
			if size>1024:size='%dMB'%(size/1024)
			else:size='%dKB'%size
			label=filename+' - %s'%size
			if os.path.isfile(joinpath(url, filename)):
				file_ext=os.path.splitext(filenamefullpath)[1][1:].lower()
				if file_ext in media_ext:
					item = xbmcgui.ListItem(label, iconImage=icon['khophim'])
					query=menuContext(label,filenamefullpath,'','',mode,query,item)
					xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=filenamefullpath,listitem=item)
				elif file_ext=='xml':addirs(label,filenamefullpath,icon['khophim'],query='xml')
				else:addirs(label,filenamefullpath,query='file')
			else:
				name='%s%s[/COLOR]'%(color['trangtiep'],filename)
				addir(name,filenamefullpath,icon['icon'],'',mode,1,filenamefullpath,True)
		return
	else:mess(u'Ch??a x??? l?? ki???u file n??y','MyFolder')
	return 'no'

def play_maxspeed_link(url):
	if not url or url=='Maxlink':
		maxlink=get_input('H??y nh???p max speed link c???a Fshare, 4share ho???c t??nl???a')
		if not maxlink or not maxlink.strip():return 'no'
		url=maxlink.replace(' ','')
	elif len(url)<13:
		fsend=getFsend(url)
		if fsend:url=fsend[0][1]
		else:mess(u'L???i get Fsend!','play_maxspeed_link');return 'no'
	return xshare_resolve(url,filmlabel='Maxlink')

def getFsend(id):
	response=make_request('http://fsend.vn/'+id,hd,'o')#http://fsend.vn/2LJL4GPVZ48L file XXOA5LADP6FC folder
	hd['Cookie']=response.cookiestring
	token=xsearch('"(.+?)"',urllib.unquote(response.cookiestring))
	data={"fs_csrf":"%s"%token,"DownloadForm[speed]":"slow","ajax":"download-form","undefined":"undefined"}
	resp=make_post('http://fsend.vn/default/download',data=urllib.urlencode(data),headers=hd)
	if resp.status==200:
		try:json=resp.json
		except:json=''
	else:json=''
	if json and json['code']==200:items=[(os.path.basename(json['url']),json['url'],'')]
	elif json and json['code']==400:
		pattern='avatar. title="(.+?)".+?<p><b>(.+?)</b></p>.+?<a href="/(.+?)"';items=[]
		for title,size,id in re.findall(pattern,response.body,re.DOTALL):items.append((title,size,id))
	else:items=[]
	return items

def tenlua_getlink(href):
	idf=xsearch('\w{14,20}',href,0)
	if not idf:return
	response=tenlua_get_detail_and_starting(idf)
	if response["type"]=="file":
		name=response['n'].encode('utf-8');url="https://www.tenlua.vn/download/"+idf
		addir(name,url,mode=3)
	elif response["type"]=="folder":
		for item in response['content']:
			tenlua_getlink(item['link'])

def id_2url(name,url,img,mode,page,query):
	def check_id_tenlua(id):
		mess('ID Checking on Tenlua.vn','',1000)
		response=tenlua_get_detail_and_starting(id);title='';img=icon['tenlua']
		if response["type"]=="file":title=response['n'];href="https://www.tenlua.vn/download/"+id
		elif response["type"]=="folder":title=response["folder_name"];href="https://www.tenlua.vn/fm/folder/"+id
		if title:return title,href,img
		else:return '','',''
	def check_id_4share(id):
		mess('ID Checking on 4share.vn','',1000)
		href='http://4share.vn/f/%s/'%id;title='';img=icon['4share']
		item=re.search('<center>.+?<strong>(.+?)</strong>.+?<strong>(.+?)</strong></center>',make_request(href))
		if item:title=item.group(1)+' - '+item.group(2)
		else:
			href='http://4share.vn/d/%s/'%id
			item=re.search("<br/><b>(.+?)</b>|<a href='(/f/\w+)|<a href='(/d/\w+)'>",make_request(href))
			if item:title,href,img=item.group(1),item.group(2),item.group(3)
		if title:return title,href,img
		else:return '','',''
	def check_id_internal(id):
		mess('ID Checking on xshare.vn','',1000)
		r1='href="(.+%s.*)" img="(.*?)">(.+?)</a>';r2='img="(.*?)" fanart=".*?" href="(.+%s.*)">(.+?)</a>'
		files='phimfshare.xml-hdvietnam.xml';title=''
		for file in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
			body=makerequest(joinpath(datapath,file));id=id.lower() if len(id)>13 else id
			items=re.search(r1%id,body) if file in files else re.search(r2%id,body)
			if items:
				title=items.group(3)
				href=items.group(1 if file in files else 2)
				img=items.group(2 if file in files else 1);break
		if title:return title,href,img
		else:return '','',''
	def check_id_fshare(id):
		mess('ID Checking on Fshare.vn','',1000)
		href='https://www.fshare.vn/file/%s'%id;body=make_request(href);title=''
		if 'class="file-info"' in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		else:
			href='https://www.fshare.vn/folder/%s'%id
			body=make_request(href)
			if 'class="filename"' in body:title=xsearch('<title>(.+?)</title>',body).replace('Fshare - ','')
		if title:return title,href,icon['fshare']
		else:return '','',''
	
	if query=='MyFshare':query=thumucrieng;page=4
	if page==0:
		name=color['search']+'Nh???p ID/link:[/COLOR] %sFshare/Fsend[/COLOR]/%s4share[/COLOR]/%stenlua[/COLOR] ho???c link %ssubscene[/COLOR]'%(color['fshare'],color['4share'],color['tenlua'],color['subscene'])
		addir(name,url,icon['icon'],mode=mode,query=query,page=1,isFolder=True)
		for href,name in re.findall('<a href="(.+?)">(.+?)</a>',makerequest(search_file)):
			q='ID?xml' if '.xml' in name else 'ID?'+query
			addirs(name,href,icon['id'],query=q)
	elif page == 1:#Nh???p ID m???i BIDXFYDOZMWF
		idf = get_input('H??y nh???p chu???i ID c???a Fshare/4share/tenlua Ho???c fulllink subscene')#;record=[]
		if idf is None or idf.strip()=='':return 'no'
		if 'subscene.com' in idf:return subscene(name,''.join(s for s in idf.split()),'subscene.com')
		idf = xsearch('(\w{10,20})',''.join(s for s in idf.split()).upper())
		if len(idf)<10:mess(u'B???n nh???p ID link ch??a ????ng: %s!'%idf);return 'no'
		title,href,img=check_id_internal(idf)
		if not title:# or True:
			title,href,img=check_id_fshare(idf)
			if not title:
				title,href,img=check_id_4share(idf)
				if not title:title,href,img=check_id_tenlua(idf)
		if title and href:make_mySearch(title,href,img,'',mode,'Add');addirs(title,href,img)
		else:mess(u'Kh??ng t??m ???????c link c?? ID: %s!'%idf);return 'no'
	elif page == 4:#M??? th?? m???c chia s??? tr??n Fshare
		title=color['search']+"M???c Link y??u th??ch c???a t??i tr??n Fshare (My fshare favorite)[/COLOR]"
		addir(title,"https://www.fshare.vn/files/favorite",img,fanart,mode=90,query='favorite',isFolder=True)
		doc_TrangFshare(name,query,iconpath+'fshare.png','')
	return ''

def ifile_tv_page(url):
	items=[]
	try: 
		pattern='id="(\d{,6})".{,300}<a href="(.+?)".{,300}src="(.+?)".{,300}"red">(.+?)</font>'
		item = re.compile(pattern,re.DOTALL).findall(make_request(url))
		for id_tip,href,img,name in item:
			http='http://ifile.tv';href=http+href;id_htm=href.rsplit('.')[2];img=http+img;name=name.strip()
			items.append((id_tip,id_htm,href,img,name))
	except:print 'ifile_tv_page Error: '+ url
	return items #id_tip,id_htm,href,img,name

def ifile_tv_4share(url):
	items = []
	body = make_request(url)
	pattern="href='/(.+?)'>.+?</a></u>|<div class='arrow_news'> <a.+>(.+?)</a>|<img src= '(.+?)' style='width: 100%'>"
	pattern+="|<b>(.+?)</b><br/><b>|<b>(http://4share.vn.+?)</b>.{,20}<b>(.+?)</b>"
	pattern+="|href='(http://subscene.com/subtitles/.+?)'"
	category=name=img=''
	for c,n1,i,n2,url4share,size,urlsubscene in re.findall(pattern,body):
		category+=xsearch('phim/(.+?)\.\d{,6}',c)+' '
		if n1:name=n1
		if n2 and not name:name=n2
		if i:img=i
		if url4share and url4share not in items:
			category=' '.join(s for s in category.split())
			name=clean_string(name)+' - '+size;url4share=urllib.unquote(url4share)
			items.append((url4share,'http://ifile.tv'+img,name,category))
		if urlsubscene and urlsubscene not in items:
			category=' '.join(s for s in category.split())
			name=clean_string(name)+' - '+size;urlsubscene=urllib.unquote(urlsubscene)
			items.append((urlsubscene,'http://ifile.tv'+img,name,category))
	return items

def ifile_update():
	mess(u'Ifile.tv auto updating ...',homnay)
	items_old=doc_xml(joinpath(datapath,"ifiletv.xml"));id_old=[s[1] for s in items_old]
	items_new = []#id_tip,id_htm,href,img,name
	for id_tip,id_htm,href,img,name in ifile_tv_page('http://ifile.tv/') :
		if id_htm not in id_old:
			for url4share,fanart,name2,catalog in ifile_tv_4share(href):
				fullname=name2 if name in name2 else name
				fullname=' '.join(s for s in fullname.split())
				items_new.append((id_tip,id_htm,catalog,img,fanart,url4share,fullname))
	if items_new:update_xml(items_new,items_old,"ifiletv.xml")
	else:mess(u'Kh??ng c?? phim m???i...','Ifile.tv auto update')
	return 'ok'

def read_all_filexml(fn="vaphim.xml",string_search='',lists=[],index=[]):
	if string_search:lists=lists+doc_xml(joinpath(datapath,fn),para='search:'+string_search)
	else:lists=lists+doc_xml(joinpath(datapath,fn))
	if not string_search:
		for id_tip,id_htm,category,img,fanart,url,name in lists:index.append((id_htm))
	return lists,index

def googleapis_search(url,query,mode):
	if '?' not in query:start='0'
	else:start=query.split('?')[1];query=query.split('?')[0]
	if url=='hdvietnam.com':url_search='https://www.googleapis.com/customsearch/v1element?rsz=filtered_cse&num=20&key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&source=gcsc&gss=.com&cx=006389339354059003744:dxv8n47myyg&googlehost=www.google.com&sig=23952f7483f1bca4119a89c020d13def&nocache&start=%s&q=%s';ico=icon['hdvietnam']
	elif url=='phimfshare.com':url_search='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&rsz=filtered_cse&num=20&hl=vi&prettyPrint=false&source=gcsc&gss=.com&googlehost=www.google.com&sig=23952f7483f1bca4119a89c020d13def&cx=005609294674567689888:qyuk9aoqwmg&nocache&start=%s&q=%s';ico=icon['phimfshare']
	else:return list()
	url_search=url_search%(start,urllib.quote_plus(query))
	result=make_request(url_search,resp='j');items=list()
	if not result:return list()
	for item in result.get("results",dict()):
		href=urllib.unquote(item.get('url'))
		if not href:continue
		name=remove_tag(item.get('titleNoFormatting'))
		if len(name.split())<2:name=os.path.basename(item['url'])
		img=get_dict(item,['richSnippet','cseThumbnail','src'])
		if not img:img=ico
		fanart=get_dict(item,['richSnippet','cseImage','src'])
		items.append((name,href,img,fanart,0,1,'get_link_post'))
	page_dict=get_dict(result,['cursor','pages']);label=list();pages=0
	if page_dict:label=[s.get('label') for s in page_dict if s.get('start')==start]
	if label:label=label[0]+1;start=[s.get('start') for s in page_dict if s.get('label')==label]
	for item in page_dict:pages=item.get('label') if item.get('label',0)>pages else pages
	if label and start:
		label=color['trangtiep']+'Trang tiep theo...trang %d/%d[/COLOR]'%(label,pages)
		items.append((label,url,ico,'',mode,4,query+'?'+start[0]))
	return items

def xshare_search(name,url,query,mode,page,items=[]):#13
	def trang_search(string):
		if len(string.split('?'))==3:p=string.split('?')[2];trang=string.split('?')[1];string=string.split('?')[0]
		elif len(string.split('?'))==2:p=1;trang=string.split('?')[1];string=string.split('?')[0]
		else:p=trang='1'
		return string,trang,p

	if url=='addstring.xshare.vn' or query=='Add':
		name=remove_tag(name)
		if not re.search(name,makerequest(search_file)):
			makerequest(search_file,'<a>%s</a>\n'%name,'a')
			mess(u'???? th??m t??n phim n??y v??o DS t??m ki???m')
	elif page==0:make_mySearch('',url,'','',mode,'get');return
	elif page==1:
		query=make_mySearch('',url,'','','','Input');page=2
		if query is None or not query.strip():return 'no'
	query=no_accent(query)
	
	if url=='vaphim.com':#print_dict(mp('http://vaphim.com/fast-search.php',data='term=hur+jun',resp='j'))
		query,trang,p=trang_search(query);hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
		url_search='http://vaphim.com/page/%s/?s=%s'%(trang,urllib.quote_plus(query))
		#body=make_request(url_search,hd)
		body=xread(url_search,hd)
		items=vp_page(url_search,body)#id,name,href,img,category
		if not items:mess(u'Kh??ng t??m ???????c t??n phim ph?? h???p!','vaphim.com search');return 'no'
		for id,name,href,img,category in items:
			addir_info(name,href,img,query='vp_getsubpage')
		page_tag=re.search("class='pages'>(.+?)<.+span><a href='(.+?)' class='page larger'>(\d{,3})</a>",body)
		if page_tag:
			trang=str(int(trang)+1)
			name=color['trangtiep']+'Tiep theo %s...trang %s[/COLOR]'%(page_tag.group(1),page_tag.group(3))
			addir_info(name,url,icon[url.split('.')[0]],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	
	elif url in 'phimfshare.com hdvietnam.com':
		items=googleapis_search(url,query,mode)
		if not items:return
		for name,url,img,fanart,mode,page,query in items:
			addir_info(name,url,img,fanart,mode,page,query)
	
	elif url=='tenlua.vn':#get_dict(dict,key_list=list(),result='')
		query,trang,p=trang_search(query)
		href='https://api2.tenlua.vn/search?keyword=%s&page=%s'%(urllib.quote_plus("%s"%query),trang)
		dict=make_request(href,resp='j')
		if int(get_dict(dict,['pagging','total'],'0'))==0:
			mess(u'Kh??ng t??m ???????c t??n phim ph?? h???p!','tenlua search');return 'no'
		for item in dict.get('items',{}):
			if item is None or item.get('ext','no') not in media_ext:continue
			id=item.get('h')
			link=tenlua_get_detail_and_starting(id)
			if link.get('type')=="none":continue
			elif link.get('type')=="file":name=link['n'];href="https://www.tenlua.vn/download/%s"%id
			elif link.get('type')=="folder":name=link["folder_name"];href="https://www.tenlua.vn/fm/folder/%s"%id
			if href not in items:items.append(href);addir_info(name,href,icon['tenlua'])
		trang=str(int(trang)+1)
		if int(get_dict(dict,['pagging','pages'],'0'))>=int(trang) and len(items)<10 and int(trang)%15>0:
			return xshare_search(name,url,'%s?%s?%s'%(query,trang,p),mode,page,items)
		p=str(int(p)+1)
		if int(get_dict(dict,['pagging','pages'],'0'))>=int(trang):
			name=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%p
			addir_info(name,url,icon['tenlua'],'',mode,4,'%s?%s?%s'%(query,trang,p),True)
	
	elif '4share.vn' in url:
		def ext_media(url):return os.path.splitext(url)[1][1:].lower().strip() in media_ext
		if url=='4share.vn':url='http://4share.vn/search?search_string='+urllib.quote_plus(query)
		pattern="<a href='(.+?)' target='_blank' title='(.+?)'>.+?</a>"
		body=xread(url);items=[s for s in re.findall(pattern,body) if ext_media(s[0])]
		if not items:mess(u'Kh??ng t??m th???y d??? li???u y??u c???u!','xshare_search');return 'no'
		for href,title in items:addir_info(title,href.split()[0],icon['4share'])
		next=xsearch("<a href='([^<]+?)'> Next</a>",body)
		if next:
			title=color['trangtiep']+'Trang tiep theo...trang %s[/COLOR]'%xsearch('\?page=(\d{1,3})&',next)
			addir_info(title,'http://4share.vn'+next.replace(' ','+'),icon['4share'],'',mode,4,'',True)
	
	elif url=='ifile.tv':
		query,trang,p=trang_search(query)	
		url_search = 'http://ifile.tv/search?search_module=phim&search_name=1&'
		url_search += 'search_content=1&time_sort=new&search_string="%s"'%urllib.quote_plus(query)
		items = []
		for content in re.findall("<td>(.*?)</b>",xread(url_search)):
			items+=re.findall("<a.+href='(.+?)'.+src='(.+?)'.+(\d{5}).+>(.+?)</a>",content)
		if not items:mess(u'Kh??ng t??m ???????c t??n phim ph?? h???p!','Ifile.tv search');return 'no'
		items_xml,id_xml = read_all_filexml(fn="ifiletv.xml")
		for href,img,id_htm,name in items:
			if id_htm in id_xml:
				index = id_xml.index(id_htm)
				while id_xml[index] == id_htm:
					temp.append((items_xml[index]));index +=1 
			else:
				for url4share,fanart,name2,catalog in ifile_tv_4share('http://ifile.tv'+href):
					temp.append(('',id_htm,catalog,img,fanart,url4share,name))
		for id_tip,id_htm,catalog,img,fanart,href,name in temp:addir_info(name,href,img,fanart)
	
	elif url=='xshare.vn':
		query,trang,p=trang_search(query);items=[]
		if trang=='1':
			for fn in ['vaphim.xml','ifiletv.xml','phimfshare.xml','hdvietnam.xml']:
				items,index=read_all_filexml(fn=fn,string_search=".*".join(query.split()),lists=items)
			items=sorted(items,key=lambda l:no_accent(l[3]).lower());p=str(len(items))
			if not items:mess(u'Kh??ng t??m th???y phim n??o c?? chu???i ph?? h???p!','Xshare search');return
			if len(items)>(rows+rows/2):makerequest(joinpath(data_path,'temp.txt'),str(items),'w')
		else:f=open(joinpath(data_path,'temp.txt'));items=eval(f.readlines()[0]);f.close()
		trang=int(trang);del items[:rows*(trang-1)]
		if len(items)>(rows+rows/2):
			del items[rows:];trang=str(trang+1)
		else:trang=''
		for img,fanart,href,name in items:addir_info(name,href,img,fanart)
		if trang:
			name=color['trangtiep']+'Trang tiep theo...trang %s/%s[/COLOR]'%(trang,str(int(p)/rows+1))
			addir_info(name,url,icon['icon'],'',mode,4,'%s?%s?%s'%(query,trang,p),True)

	elif 'taifile.net' in url:
		def taifile_search(url):
			q=xread(url);vp=[]
			for s in re.findall('(<div class="bgframe">.+?</a></div></div>)',q):
				if not 'fshare.vn' in s:continue
				title=xsearch('title="(.+?)"',s)
				size=xsearch('Size: <b>(.+?)</b>',s)
				title='[COLOR gold]Fshare[/COLOR] '+title.replace('Download ','')+ ' - '+size
				href='http://www.taifile.net'+xsearch('href="(/x.php\?id=.+?)"',q)
				link=xsearch('href="(http://vaphim.com[^<]+?)"',s)
				label=xsearch('title="([^"]+?)" target',s)
				addir_info(title,href,icon['taifile'],'',mode,4,'play')
				if link and link not in str(vp):vp.append((link,label))

			for link,label in vp:
				addir_info('[COLOR gold]'+label+'[/COLOR]',link,icon['vaphim'],'',1,1,'vp_getsubpage',True)

			pn=re.search('<a class="active" href="[^<]+?">\d+?</a><a href="([^<]+?)">(\d+?)</a>',q)
			if pn:
				href=pn.group(1).replace('amp;','').replace('/search.php?q=','')
				href='http://www.taifile.net/search.php?q='+'%20'.join(s for s in href.split())
				title=color['trangtiep']+' Trang tiep theo...trang %s[/COLOR]'%pn.group(2)
				addir_info(title,href,icon['taifile'],'',mode,4,'search',True)
		
		if query=='search':taifile_search(url)
		elif query=='play':
			b=make_request(url,resp='o')
			if b and b.getheader('location'):resolve_url(b.getheader('location'))
		else:
			b=make_post('http://www.taifile.net/suggest.php',data={'q':query},resp='j')
			if not b or len(b)<2:
				href='http://www.taifile.net/search.php?&host=fshare&q='+urllib.quote_plus(query)
				taifile_search(href)
			else:
				if '/search.php?q='+query not in b:b[query]=query
				for i in b:
					title='[COLOR lime]Search on:[/COLOR] '+' '.join(s for s in re.sub('<.*?>|\[.*?\]|\(.*?\)','',b.get(i)).split())
					href='http://www.taifile.net/search.php?&host=fshare&q='+urllib.quote(i.replace('/search.php?q=',''))
					addir_info(title,href,icon['taifile'],'',mode,4,'search',True)
	return ''

def pfs_update():
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');pfs_update_time=my_dict.get('pfs_update_time','0')
	if int(timenow)-int(pfs_update_time)<5:return
	else:my_dict['pfs_update_time']=timenow;my_dict=json_rw('xshare.json',my_dict)
	mess(u'PhimFshare.com auto updating ...',homnay)
	body=make_request('http://phimfshare.com/external.php?type=RSS2');items=list()
	if not body:return
	phimfshare=makerequest(joinpath(datapath,'phimfshare.xml'));string='';count=0
	for item in re.findall('<item>(.+?)</item>',body,re.DOTALL):
		id=xsearch('<link>.*-(\d{5,6})/.*</link>',item)
		if not id:continue
		title=re.sub('<!\[CDATA\[|\]\]>','',xsearch('<title>(.+?)</title>',item))
		img=xsearch('img src="(.+?jpg)["|?| ]',item)
		content=xsearch('<content:encoded>(.+?)</content:encoded>',item,1,re.DOTALL)
		pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14}|http://4share.vn/./\w{14,20}|https?://w?w?w?/?tenlua.vn/.*?|http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for href in list(set([s for s in re.findall(pattern,content) if '..' not in s])):
			href=correct_link(href);server=xsearch('(\w{6,8})\.[v|c]',href)
			if href not in phimfshare:
				string+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(id,server,href,img,title);count+=1
	if string:
		mess(u'???? c???p nh???t ???????c %d phim'%count,'Phimfshare auto update')
		makerequest(joinpath(datapath,'phimfshare.xml'),string,'a')
	else:mess(u'Kh??ng c?? phim m???i','Phimfshare auto update')

def pfs_getlink(content):#6+
	items=[]
	pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]'
	for links in re.findall(pattern,content):
		if links:
			for link in links:
				idf=xsearch('(\w{10,20})',link)
				if idf:
					link=link.lower()
					if 'fshare.vn/file' in link:url='https://www.fshare.vn/file/%s'%idf.upper();server="fshare"
					elif 'fshare.vn/folder' in link:url='https://www.fshare.vn/folder/%s'%idf.upper();server="fshare"
					elif 'tenlua.vn' in link and ('folder/' in link or '#download' in link) and len(idf)>16:
						url='https://tenlua.vn/fm/folder/%s'%idf;server="tenlua"
					elif 'tenlua.vn' in link and len(idf)>16:url='https://tenlua.vn/download/%s'%idf;server="tenlua"
					elif '4share.vn' in link:url=link;server="4share"
					else:continue
					items.append((server,url))
	return items

def subtitle_of_year(title):
	string=re.split('20\d\d|19\d\d',title)[0]
	string=re.sub(xsearch('multi ',string,0,re.IGNORECASE),'',string)
	return string if string else title

def phimFshare(name,url,img,fanart,mode,page,query):#6
	fphimfshare=joinpath(datapath,'phimfshare.xml');home='http://phimfshare.com/';pagenext=''
	def pfs_page(url,pattern):
		body=make_request(url)
		return re.findall(pattern,body),xsearch('<a rel="next" href="(.+?)" title=".+?">',body)
	def pfs_addir(items):
		for id,href,img,name in items:addirs(name,href,img)
	def pfs_xml():
		pattern='<a id="(.+?)" server=".+?" href="(.+?)" img="(.*?)">(.+?)</a>'
		return re.findall(pattern,makerequest(fphimfshare))
	
	if query=='phimfshare.com':make_mySearch('',url,'','',mode,'get');return
	elif page==4 and name==query:return phimFshare('Search',url,img,fanart,mode,page,query)
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		return phimFshare('Search',url,img,fanart,mode,page,query) if query else 'no'
	elif name=='Search':
		items=googleapis_search('phimfshare.com',query,mode)
		items=[(s[2],s[1],'',s[0]) for s in items if 'Trang tiep theo' not in s[0]]
		if not items:mess(u'Kh??ng t??m th???y phim c?? ch???a chu???i t??m ki???m!','phimFshare');return 'no'
	elif query=='get_link_post':
		response=make_request(url)
		img=xsearch('<img src="(.+?)" border="0" alt="" />',response)
		for server,href in pfs_getlink(response):addir_info(re.sub('\[/?COLOR.*?\]','',name),href,img)
		return
	elif query=='PhimMoi':
		items,pagenext=pfs_page(home,'()<a href="(.+?)" ()class="title">(.+?)</a>')
	elif url=='folder':pfs_addir([s for s in pfs_xml() if query in s[3]]);return
	else:
		if home not in url:url=home+url+'/'
		pattern='<img class="preview" src="(.+?)" .+? class=".+?" href="(.+?)" id="thread_title_(.+?)">(.+?)</a>'
		items,pagenext=pfs_page(url,pattern)#img,href,id,title
		
	items=[(s[0],s[1],s[2] if len(s[2])>4 else xsearch('-(\d{5})',s[1]),s[3]) for s in items]
	lists=[s for s in pfs_xml() if s[0] in [f[2] for f in items]]
	for label in list(set([subtitle_of_year(s[3]) for s in lists])):
		temp=[s for s in lists if label in s[3]]
		if not temp:continue
		elif len(temp)>1:
			id,href,img,title=temp[0];title=[s[3] for s in temp if '~' in s[3]]
			title=label+' ~ '+re.sub('.+?~ ?','',title[0]) if title and '~' not in label else label
			addir(color['phimfshare']+title+'[/COLOR]','folder',img,'',mode,page,label,True)
		else:pfs_addir(temp)
	if pagenext:
		page=2 if not page else page+1
		label=color['trangtiep']+'Trang ti???p theo - Trang '+str(page)+' ...[/COLOR]'
		addir(label,pagenext,iconpath+'fshare.png',mode=mode,page=page,query=query,isFolder=True)
	if name=='Search':return
	endxbmc();ids=[s[2] for s in items if s[2] not in list(set([f[0] for f in lists]))];content_new=''
	if ids:mess(u'Databse updating...','phimfshare.com')
	for img,href,id,name in [s for s in items if s[2] in ids]:
		response=make_request(href)
		temp=xsearch('<title> (.+?)</title>',response)
		if temp:name=temp
		elif not name:continue
		if not img:img=xsearch('<img src="(.+?)" border="0" alt="" />',response)
		name=' '.join(s for s in re.sub('\[.+?\]|\(.+?\)|MuLtI|Fshare|fshare','',name).split())
		for server,link in pfs_getlink(response):
			if link not in content_new:
				content_new+='<a id="%s" server="%s" href="%s" img="%s">%s</a>\n'%(id,server,link,img,name)
	if content_new:makerequest(fphimfshare,content_new,'a');xbmc.executebuiltin("Container.Refresh")
	return ''

def correct_link(url):
	if 'tenlua.vn' in url:idf=xsearch('(\w{16,20})',url)
	elif 'subscene.com' in url and '...' not in url:idf='ok'
	else:idf=xsearch('(\w{10,20})',url)
	if idf:
		url=url.lower()
		if 'fshare.vn/file' in url:url='https://www.fshare.vn/file/%s'%idf.upper()
		elif 'fshare.vn/folder' in url:url='https://www.fshare.vn/folder/%s'%idf.upper()
		elif 'tenlua.vn' in url and ('folder/' in url or '#download' in url) and len(idf)>16:
			url='https://tenlua.vn/fm/folder/%s'%idf
		elif 'tenlua.vn' in url and len(idf)>16:url='https://tenlua.vn/download/%s'%idf
		elif '4share.vn' or 'subscene.com'in url:url=url
	else:url=''
	return url

def hdvn_update(items=[]):#33-146-311-265-110-116-123-57-157
	mess(u'HDVietnam.com auto updating ...',homnay)
	urlhome='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids='
	if not items:
		pattern='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for id in '-33-146-311-265-110-116-123-57-157'.split('-'):
			mess('hdvietnam forumids=%s updating ...'%id,homnay)
			for name,link,pubDate,img,description,uploader in hdvietnam_rss(urlhome+id):
				for links in re.findall(pattern,description):
					for href in [s for s in links if s and '...' not in s]:
						href=correct_link(href)
						if href not in str(items):items.append((href,img,name))
	file=joinpath(datapath,"hdvietnam.xml");string='';count=0
	urls=re.findall('href="(.+?)"',makerequest(file))
	for url,img,name in [s for s in items if s[0] not in urls]:
		string+='<a date="%s" href="%s" img="%s">%s</a>\n'%(homnay,url,img,name);count+=1
	if string:
		makerequest(file,string,'a')
		mess(u'???? c???p nh???t ???????c %d phim'%count,'hdvietnam update')
	else:mess(u'Kh??ng c?? phim m???i','hdvietnam update')
	return 'ok'

def hdvietnam_rss(url):
	body=xread(url);items=list()
	for data in re.findall('<item>(.+?)</item>',body,re.DOTALL):
		label=xsearch('<title><!\[CDATA\[(.+?)\]\]></title>',data)
		link=xsearch('<link>(.+?)</link>',data)
		pubDate=xsearch('<pubDate>(.+?)</pubDate>',data)
		description=xsearch('<description><!\[CDATA\[(.+?)\]\]></description>',data,1,re.DOTALL)
		uploader=xsearch('<dc:creator>(.+?)</dc:creator>',data);img=''
		for img in re.findall('Image: (http.+?\.jpg|http.+?\.png)',data):
			if not [s for s in ['kho-phim','chuyenlink.php','header-'] if s in img]:break
		items.append((label,link,pubDate,img,description,uploader))
	return items

def hdvietnam(name,url,img,fanart,mode,page,query):
	ico=icon['hdvietnam'];tempfolder=xbmc.translatePath('special://temp')
	urlhome='http://www.hdvietnam.com/diendan/';c='orangered'
	from resources.lib.servers import hdvn;hdvn=hdvn()
	menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
	menu['MyFshare']={'action':'Add','server':['fshare.vn']}
	menu['MyFavourites']={'action':'Add','server':['fshare.vn','4share.vn','tenlua.vn','subscene.com']}
	
	if url in '000-UPD':
		if query=='UPD':hdvn_update()
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));homqua=''
		if not body:return
		dates=sorted(list(set(re.findall('date="(.+?)"',body))),key=lambda k:k[6:]+k[3:5]+k[:2],reverse=True)
		homnay=dates[0] if query in '000-UPD' else query
		items=re.findall('date="%s" href="(.+?)" img="(.+?)">(.+?)</a>'%homnay,body)
		for name in list(set([subtitle_of_year(s[2]) for s in items])):
			lists=[s for s in items if name in s[2]]
			if not lists:continue
			elif len(lists)==1:
				href,img,title=lists[0]
				addir_info(title,href,img,'',mode,1,'',True,menu=menu)
			else:
				href,img,title=lists[0]
				title=name+' ~ '+re.sub('.+?~ ?','',title) if '~' in title and '~' not in name else name
				addir_info(title,'hdvietnam.com',img,'',mode,1,name,True,menu=menu)
		if dates.index(homnay)+1<len(dates):
			homqua=dates[dates.index(homnay)+1]
			name=color['trangtiep']+"Th??ng tin ng??y %s[/COLOR]"%homqua
			addir_info(name,"000",ico,'',mode,1,homqua,True)
	
	elif query=='get_room_id':
		id=get_input('H??y nh???p chu???i ID Room c???a hdvietnam.com')
		if not id or not id.strip():return 'no'
		url='http://www.hdvietnam.com/diendan/showthread.php?t=%s'%id
		return hdvietnam(name,url,img,fanart,mode,page,'get_link_post')
	
	elif 'muctheodoi' in query:
		if 'Add' in query:hdvn.addRoom(url)
		elif 'Remove' in query:
			if hdvn.removeRoom(url):xbmc.executebuiltin("Container.Refresh")
		else:
			menu={'muctheodoi':{'action':'Remove','server':['hdvietnam.com']}}
			if query=='muctheodoi':url='http://www.hdvietnam.com/diendan/subscription.php?folderid=0'
			content=hdvn.getpage(url,loop=True)
			for href,title in re.findall('<a class="title.*?" href="(.+?)" id=".+?">(.+?)</a>',content):
				addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'get_link_post',True,menu=menu)
	
	elif url=='hdvietnam.com':
		body=makerequest(joinpath(datapath,"hdvietnam.xml"));temp=[]
		items=[s for s in re.findall('date=".+?" href="(.+?)" img="(.+?)">(.+?)</a>',body) if query in s[2]]
		for href,img,name in list(set(items)):
			if href not in temp:
				temp.append(href)
				addir_info(name,href,img,menu=menu)

	elif re.search('\d\d',query):
		url='http://www.hdvietnam.com/diendan/external.php?type=RSS2&forumids=%s'%query
		items=list();page=-1
		rss_list=hdvietnam_rss(url)
		if not rss_list:mess(u"H??m nay ch??a t??m th???y n???i dung RSS n??y!","hdvietnam.com");return
		for label,link,pubDate,img,description,uploader in rss_list:
			items.append(description);page+=1
			name='[COLOR gold]%s[/COLOR] [COLOR lime]%s[/COLOR]:: %s'%(uploader,pubDate,label)
			addir_info(name,link,img,'',mode,page,'read_rss',True)
			if xsearch('/(\d{6,10})-',link):
				href='http://www.hdvietnam.com/diendan/showthread.php?t='+xsearch('/(\d{6,10})-',link)
			else:href=link
			addir_info(namecolor('?????n trang ',c)+os.path.basename(link),href,img,'',mode,1,'get_link_post',True,menu=menu)
			addir_info(namecolor(remove_tag(label),c),link,img,'',mode,page,'read_rss',True,menu=menu)
		temp=makerequest(joinpath(tempfolder,"hdvietnam.rss"),str(items),'w')

	elif query=='read_rss':
		items=list();name=remove_tag(name)
		try:content=eval(makerequest(joinpath(tempfolder,"hdvietnam.rss")))[page]
		except:content=''
		pattern1='<a href="(.+?hdvietnam.com.+?|.+?fshare.vn.+?|.+?4share.vn.+?|.+?tenlua.vn.+?|.+?subscene.com.+?)" target="_blank">(.+?)</a>'
		pattern2='(https?://www.fshare.vn/\w{4,6}/\w{10,14})|(http://4share.vn/./\w{14,20})|(https?://w?w?w?/?tenlua.vn/.*?)[ |"|<]|(http://subscene.com/subtitles/.+?)[ |"|\'|<]'
		for href,title in re.findall(pattern1,content):
			if any(s for s in ['fshare.vn/','4share.vn/','tenlua.vn/','subscene.com/'] if s in title):
				items.append((0,name,href,img))
			elif 'http://' not in title:items.append((1,remove_tag(title),href,img))
		for links in re.findall(pattern2,content):
			for link in [s for s in links if s and '...' not in s]:
				if link not in str(items):items.append((0,name,link,img))
		for title,href,img in [(s[1],s[2].replace('amp;',''),s[3]) for s in sorted(items)]:
			addir_info(title,href,img,query='get_link_post',menu=menu)

	elif query=='MCS':
		body=hdvn.getpage('http://www.hdvietnam.com/diendan/34-chia-se-phim/?styleid=25')
		for href,name in re.findall('<h3><a href="(.+?)">(.+?)</a></h3>',body):
			addir_info(namecolor(name,c),urlhome+href.split('&')[0],img,query='PL1')

	elif query=='CSN':
		body=hdvn.getpage('http://www.hdvietnam.com/diendan/148-chia-se-nhac/?styleid=25')
		for href,name in re.findall('<h3><a href="(.+?)">(.+?)</a></h3>',body):
			addir_info(namecolor(name,c),urlhome+href.split('&')[0],img,query='PL1')

	elif query=='PL1':
		parent_path='http://www.hdvietnam.com/diendan/'
		if '&styleid=9' not in url:url=url+'&styleid=9'
		hd['Referer']='http://www.hdvietnam.com/diendan/'
		body=xread(url.replace('amp;',''),hd)
		if not body:body=xread(url.replace('amp;',''),hd)
		if page<2:#Ph??? M???c
			for href,title in re.findall('<a href="(forumdisplay.php.+?)">(.+?)</a></h2>',body):
				href=parent_path+href;title=title.replace(', ',' - ')
				addir_info('[B]'+namecolor(title,c)+'[/B]',href,ico,'',mode,1,'PL1',True)
		
		#Normal Threads
		pattern='<a class="title" href="(showthread.php.+?)&.+?>(.+?)</a>.+?<b>(.+?)</span>'
		menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
		body=xsearch('(Normal Threads.+?<span class="shade">)',body,1,re.DOTALL)
		
		for s in re.findall('(<h3 class="threadtitle">.+?<div class="threaddetails td">)',body,re.DOTALL):
			href=parent_path+xsearch('class="title[^"]*" href="(.+?)"',s)
			title=remove_tag(xsearch('<a class="title[^"]*"[^<]+?>(.+?)</a>',s))
			bossroom=remove_tag(xsearch('<b>(.+?)</span>',s))
			title='[COLOR yellow]%s[/COLOR]-%s'%(bossroom,namecolor(title,c))
			addir_info(title,href,ico,'',mode,1,'get_link_post',True,menu=menu)
			
		pages=xsearch('class="popupctrl">Trang \d{1,4}/(\d{1,4})</a></span>',body)
		page=2 if page<2 else page+1
		if pages and int(pages)>page:
			name=color['trangtiep']+'Trang tiep theo...trang %d%s[/COLOR]'%(page,('/'+pages) if pages else '')
			if '&page=' not in url:url=url+'&page=%d'%page
			else:url=re.sub('&page=\d{1,3}','&page=%d'%page,url)
			addir_info(name,url,ico,'',mode,page,'PL1',True)
	
	elif query=='get_link_post':
		temp='';roomid=xsearch('t=(\d+)',url) if xsearch('t=(\d+)',url) else xsearch('(\d{6,10})',url)
		add_sep_item('-%s-'%namecolor(name).replace('HDVN','Room:').replace('?????n trang ',''))
		
		if roomid:
			url='http://www.hdvietnam.com/diendan/showthread.php?t='+roomid;print 'get_link_post: %s'%url
			buian='BuiAn' if 'Xem g?? h??m nay' in name else ''
			for title,href,img in hdvn.getlink(url,buian):
				if 'http' not in href:href=urlhome+href
				if img=='morethread':
					if not temp:add_sep_item('C??c ch??? ????? c??ng chuy??n m???c')
					img=ico;temp='added_sep_item'
				query='download' if 'subscene.com' in href else 'get_link_post'
				addir_info(title,href,img,'',mode,1,query,menu=menu)#query=download cho subscene
		else:
			content=hdvn.getpage(url,loop=True)
			for href,title in re.findall('<a class="title.*?" href="(.+?)" id=".+?">(.+?)</a>',content):
				addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'get_link_post',True,menu=menu)

def database_download():
	mess(u'??ang ki???m tra v?? download database cho xshare','database_download');delete_files(tempfolder)
	tempfile = joinpath(tempfolder,"xshare_data.zip");pattern='<title>.*xx(.+?)xx.*</title>'
	if not os.path.exists(datapath):os.mkdir(datapath)
	if not os.path.exists(iconpath):os.mkdir(iconpath)
	id=xsearch(pattern,make_request('https://www.fshare.vn/folder/9F3VWL147DYG'))
	response=make_request('https://docs.google.com/uc?id=%s&export=download'%id,resp='o',maxr=1)
	if  response.status==200:
		body=makerequest(tempfile,response.body,'wb');xbmc.sleep(500)
		try:xbmc.executebuiltin('XBMC.Extract("%s","%s")'%(tempfile,tempfolder), True)
		except:mess(u'Database download error!','database_download');return
		xml_size=dict();png_size=dict()
		for file in os.listdir(datapath):xml_size[file]=os.path.getsize(joinpath(datapath,file))
		for file in os.listdir(iconpath):png_size[file]=os.path.getsize(joinpath(iconpath,file))
		for file in os.listdir(tempfolder):
			if os.path.isfile(joinpath(tempfolder,file)):
				if '.xml' in file:
					a=makerequest(joinpath(tempfolder,file));s=a.splitlines()
					a=makerequest(joinpath(datapath,file));d=a.splitlines();w=False
					for i in s:
						if i not in d:d.append(i);w=True
					if w:a='';makerequest(joinpath(datapath,file),'\n'.join(i for i in d),'w')
				elif '.xml' in file and xml_size.get(file,0)<os.path.getsize(joinpath(tempfolder,file)):
					rename_file(joinpath(tempfolder,file),joinpath(datapath,file))
				elif '.png' in file and png_size.get(file,0)!=os.path.getsize(joinpath(tempfolder,file)):
					rename_file(joinpath(tempfolder,file),joinpath(iconpath,file))
				elif '.jpg' in file and os.path.getsize(joinpath(tempfolder,file))!=613866:
					rename_file(joinpath(tempfolder,file),joinpath(home,file))
		if os.path.isfile(joinpath(data_path,'checkdatabase.txt')):os.remove(joinpath(data_path,'checkdatabase.txt'))
		myaddon.setSetting('checkdatabase','false');mess(u'Download database cho xshare th??nh c??ng','database_download')
	else:mess(u'Download database cho xshare kh??ng th??nh c??ng!','database_download')

def xshare_auto_update():
	try:
		if checkupdate('last_update.dat',17,datapath):
			xshare_update();vp_make_datanew();vp_update();ifile_update()
			makerequest(joinpath(datapath,"last_update.dat"),'','w')
			mess('Xshare auto update completed','vaphim ifiletv')
		#if checkupdate('phimfshare.xml',11,datapath):pfs_update()
		if checkupdate('hdvietnam.xml',7,datapath):hdvn_update()
	except:mess('Data update error!')

def checkupdate(filename,hours=1,folder=datapath,xdict=dict()):
	filecheck=joinpath(folder,filename);timeformat='%Y%m%d%H'
	filetime=os.path.getmtime(filecheck) if os.path.isfile(filecheck) else 0
	last_update=datetime.datetime.fromtimestamp(filetime).strftime(timeformat)
	timenow=datetime.datetime.now().strftime(timeformat)
	#if int(timenow)-int(last_update)>hours:
	#	xshare_dict=json_rw('xshare.json');file_time=xshare_dict.get(filename,'0')
	#	if timenow > file_time:xshare_dict[filename]=timenow;json_rw('xshare.json',xshare_dict);result=True
	return (int(timenow)-int(last_update))>hours

def xshare_update():
	timenow=datetime.datetime.now().strftime('%Y%m%d%H')
	my_dict=json_rw('xshare.json');time_xshare=my_dict.get('time_xshare','0')
	if int(timenow)-int(time_xshare)<24*7:return
	room_id=my_dict.get('room_id') if my_dict.has_key('room_id') else '997745'
	url='http://www.hdvietnam.com/diendan/showthread.php?t=%s&mode=threaded&styleid=9'%room_id
	items=re.findall('writeLink\((.+?),.+?,.+?, (.+?),',make_request(url,maxr=1));temp=False
	for post_id in [s[0] for s in items if s[1]=='528657' and not my_dict.has_key(s[0])]:
		my_dict[post_id]='';temp=True
	if not temp:my_dict['room_id']='997745' if room_id=='947935' else '947935'
	my_dict['time_xshare']=timenow;json_rw('xshare.json',my_dict)

def xshare_postks(body,hd,token):
	if myaddon.getSetting('usernameh')=='thaitni':return body,token,hd['Cookie']
	my_dict=json_rw('xshare.json');url='http://www.hdvietnam.com/diendan/post_thanks.php'
	for post_id in my_dict:
		if not my_dict[post_id]:
			response=make_post(url,hd,'do=post_thanks_add&using_ajax=1&p=%s&securitytoken=%s'%(post_id,token))
			my_dict[post_id]='Y';json_rw('xshare.json',my_dict);break
	return body,token,hd['Cookie']

def write_trans(fo,string,m):
	translist=google_trans(string);j=0
	for i in m:
		if i=='xshare':
			try:fo.write(translist[j].strip()+'\n');j+=1
			except:pass
		else:fo.write(i)
    
def google_trans(s):
	hd={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.8,vi;q=0.6','Cookie':''}
	url='https://translate.google.com.vn/translate_a/single?oe=UTF-8&tl=vi&client=t&hl=vi&sl=en&dt=t&ie=UTF-8&q=%s'%s
	body= xread(url,hd)
	body=body.replace(',,"en"','').replace('[[[','').replace(']]]','')
	result=''
	for i in body.split('],['):
		research=re.search('"(.+?)","(.+?)"',i)
		if research:result+=research.group(1)+' '
		else:print '%s :not research'%i
	return result.replace('Xshare','xshare').split('xshare')

def subscene(name,href,query):
	if not re.search('\d{5,10}',href):
		if not os.path.basename(href):href=os.path.dirname(href)
		pattern='<a href="(/subtitles/.+?)">\s+<span class=".+?">\s*(.+?)\s+</span>\s+<span>\s+(.+?)\s+</span>'
		body=make_request(href.replace('amp;',''),headers={'Cookie':'LanguageFilter=13,45'})
		subs=re.findall(pattern,body)
		if not subs:
			temp=xsearch('<a href="(.+?)"',xsearch('<h2 class="exact">Exact</h2>(.+?)</ul>',body,1,re.DOTALL))
			if temp:
				body=make_request('http://subscene.com'+temp,headers={'Cookie':'LanguageFilter=13,45'})
				subs=re.findall(pattern,body)
		mess(u'T??n phim: %s'%s2u(name).replace('[COLOR green]Subscene[/COLOR]-',''))
		for url,lang,name in sorted(subs,key=lambda l:l[1], reverse=True):
			name='Eng.'+name if '/english/' in url else '[COLOR red]Vie.[/COLOR]'+name
			addirs(name,'http://subscene.com'+url,query='download')
		return ''
	pattern='<a href="(.+?)" rel="nofollow" onclick="DownloadSubtitle.+">'
	downloadlink='http://subscene.com' + xsearch(pattern,make_request(href))
	if len(downloadlink)<20:mess(u'Kh??ng t??m ???????c maxspeed link sub!')
	else:xshare_resolve(downloadlink)
	return 'ok'

def megabox(name,url,img,fanart,mode,page,query):
	homepage='http://phim.megabox.vn/';ico=icon['megabox']
	cat={1:'Phim l???',2:'Phim b???',3:'Show',4:'Clip'}
	gen={1:'H??nh ?????ng',2:'Phi??u l??u',3:'Ma kinh d???',4:'T??nh c???m',5:'Ho???t h??nh',6:'V?? thu???t',7:'H??i',8:'T??m l??',9:'Ki???m hi???p',10:'S??? thi',11:'',12:'',13:'H??nh s???',14:'',15:'??m nh???c',16:'Khoa h???c',17:'T??i li???u',18:'Gia ????nh',21:'Chi???n tranh',22:'Th??? thao',25:'?????c-L???',27:'Khoa h???c vi???n t?????ng',28:'???m th???c',29:'Th???i trang',30:'??i???n ???nh',31:'Thi???u nhi',32:'Gi??o d???c',33:'TV-Show',34:'Live Show',36:'C??ng ngh???',37:'Kh??m ph?? th??? gi???i',38:'?????ng v???t',39:'Shock'}
	country={1:'??u-M???',2:'H??n Qu???c',3:'H???ng K??ng',4:'Trung Qu???c',5:'Nh???t B???n',6:'Th??i Lan',7:'Qu???c Gia kh??c',8:'M???',9:'Ph??p',11:'Vi???t Nam',12:'???n ?????',13:'Philippines'}#get(url,headers=hd,maxr=2)
	def namecolor(label):return color['megabox']+label+'[/COLOR]'
	def get_id(url):return xsearch('-(\d{1,6})\.html',url)
	def duration(string):return xsearch('Th???i l?????ng:<.+?> (.+?)</li>',string)
	def countview(string,tag='span'):return xsearch('class=.count-view.><%s></%s> (.+?)</span>'%(tag,tag),string)
	def thuyetminh(string):return color['subscene']+'TM[/COLOR] ' if xsearch('class=.ico-sub.',string,0) or string=='TM' else ''
	def phim18(string):return '[COLOR red][B]M+[/B][/COLOR] ' if xsearch('class=.ico-rating.',string,0) or string=='M+' else ''
	def episode(string):return xsearch('class=.esp.><i>(.+?)</span>',string).replace('</i>','')
	def update_dict(dict):
		body=make_request(homepage,headers=hd)
		#(phim-le,Phim l???),(phim-bo,Phim b???),(show,Show),(clip,Clip)
		dict['MGB1']=re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body)
		#(L??? B??? Show Clip M???i Nh???t, Chi???u R???p) (Megabox gi???i thi???u, Top 10, s???p chi???u, l???-b???-show-clip xem nhi???u)
		dict['MGB2']=re.findall('"H2title">(.+?)</h2>',body)
		content=sub_body(body,'id="phimle"','id="phimbo"')
		dict['phim-letl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Qu???c gia')])
		dict['phim-leqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Qu???c gia'):])
		content=sub_body(body,'id="phimbo"','id="tvshow"')
		dict['phim-boqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Th??? Lo???i')])
		dict['phim-botl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Th??? Lo???i'):])
		content=sub_body(body,'id="tvshow"','id="clip"')
		dict['showtl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[:content.find('Qu???c gia')])
		dict['showqg']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content[content.find('Qu???c gia'):])
		content=sub_body(body,'id="clip"','class="search-toogle"')
		dict['cliptl']=re.findall("title='(.+?)'.{1,3}href='(.+?)'",content)
		dict['gioithieu']=re.findall("<li><a href='(.+?)'",sub_body(body,'class="hotFilmSlider"','id="bx-pager"'))
		dict['top10']=re.findall('href="(.+?)"',sub_body(body,'begin topFilm','end topFilm'))
		dict['sapchieu']=re.findall("<a href='(.+?)'>",sub_body(body,'Phim s???p chi???u','end primary'))
		for i in range(1,5):
			s1='id="subCate-%d"'%i;s2='id="ul-%d"'%i
			dict['subCate%d'%i]=re.findall('data=.(.+?). data1=.(.+?).>(.+?)</a>',sub_body(body,s1,s2))
		return json_rw('megabox.json',dict)
	def get_detail(urls,dict):
		mess('Database updating ...','megabox.vn')
		for url in urls:
			id=get_id(url);body=sub_body(make_request(url,maxr=3),'begin primary','end primary');tm='TM' if thuyetminh(body) else ''
			views=countview(body);esp=xsearch('S??? t???p <i>(.+?)</i>',body);p18='M+' if phim18(body) else ''
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if not items:continue
			elif len(items)==1:title=items[0][0];fanart=img=items[0][1]
			else:title=items[0][0];fanart=items[0][1];img=items[1][1]
			if esp:series='y'
			else:series='n';esp=duration(body)
			dict[id]=(series,title,img,fanart,views,esp,tm,p18)
		return dict
	def json_rw1(dicts={}):
		if dicts:makerequest(joinpath(datapath,'megabox.json'),json.dumps(dicts),'w')
		else:
			try:dicts=json.loads(makerequest(joinpath(datapath,'megabox.json')))
			except:dicts={}
		return dicts
	def load_urls(urls):
		dict=json_rw('megabox.json');urls_old=[];urls_new=[];ids=[];update=False
		for url in urls:
			id=get_id(url)
			if not id:continue
			elif dict.has_key(id) and dict[id]:urls_old.append(url)
			else:urls_new.append(url)
			ids.append((id,url))
		if urls_new:dict=get_detail(urls_new,dict)
		for id,url in ids:
			try:tm=thuyetminh(dict[id][6])+phim18(dict[id][7])
			except:tm=''
			if len(dict[id])<8:dict.pop(id);continue
			img=dict[id][2];fanart=dict[id][3]
			if dict[id][0]=='y':
				epi=xsearch('(.+?)\W(.*?)\Z',dict[id][5]);eps=xsearch('(.+?)\W(.*?)\Z',dict[id][5],2)
				title=namecolor(dict[id][1])+color['subscene'];query='1episode'+eps;isFolder=True
				title=title+' - %s views:%s[/COLOR]'%(dict[id][5],dict[id][4])
			else:
				title=dict[id][1]+color['subscene']+' - (%s - views:%s)[/COLOR]'%(dict[id][5],dict[id][4].strip())
				query='mgbplay';isFolder=False
			addir(tm+title,url,img,fanart,mode,1,query,isFolder=isFolder)
		if urls_new:endxbmc();json_rw('megabox.json',get_detail(urls_old,dict));mess('Database updated','megabox.vn')
	def put_items(items,tag='span'):#class='count-view'><span></span> 551</span>
		dict=json_rw('megabox.json');cl=color['subscene']
		href_old=[s[0] for s in items if get_id(s[0]) in dict]
		href_new=[s[0] for s in items if s[0] not in href_old]
		for href,name,dura,img,esp,view in items:
			id=get_id(href);views=countview(view,tag);dura=duration(dura)
			tm=thuyetminh(esp)+phim18(esp);esp=episode(esp);eps=xsearch('\W(.*)\Z',esp)
			if esp:title,query,series,isFolder=namecolor(name),'1episode'+eps,'y',True
			else:title,esp,query,series,isFolder=name,dura,'mgbplay','n',False
			title=tm+title+' %s%s views: %s[/COLOR]'%(cl,esp,views)
			try:fanart=dict[id][3] if href in href_old else img
			except:fanart=img
			p18='M+' if 'M+' in tm else '';tm='TM' if 'TM' in tm else ''
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
			addir(title,href,img,fanart,mode,1,query,isFolder)
		return href_new,dict
	def update_href_new(hrefs,dict):
		mess('Database updating ...','megabox.vn')
		for href in href_new:
			id=get_id(href);body=sub_body(make_request(href,maxr=3),'begin primary','end primary')
			items=re.findall('alt=\'(.+?)\' src="(.+?)"',body)
			if len(items)<2:continue
			series,name,img,fanart,views,esp,tm,p18=dict[id];fanart=items[0][1];img=items[1][1]
			dict[id]=(series,name,img,fanart,views,esp,tm,p18)
		json_rw('megabox.json',dict);mess('Database updated','megabox.vn')

	def homehtml(update=False):
		if update:
			body=make_request(homepage)
			if body:makerequest(joinpath(xsharefolder,'megabox.html'),body,'w')
		else:
			body=makerequest(joinpath(xsharefolder,'megabox.html'))
			if not body:return homehtml(True)
		return body

	if url=='megabox.vn':
		label=labelsearch("Search tr??n megabox.vn")
		addir_info(label,homepage,ico,'',mode,1,'makeitemsearch',True)
		body=homehtml()
		for href,label in re.findall('<li><a href="(.+?)" title="">(.+?)</a></li>',body):
			addir_info(namecolor(label),homepage+href,ico,'',mode,1,'mainmenu',True)
		add_sep_item('N???i dung chi ti???t trang ch???')
		for label in re.findall('<h2 class="H2title">(.+?)</h2>',body):
			addir_info(namecolor(remove_tag(label)),homepage,ico,'',mode,1,'mainpage',True)
		if checkupdate('megabox.html',1,xsharefolder):endxbmc();body=homehtml(True);xbmc.executebuiltin("Container.Update")
	
	elif query=='makeitemsearch':search_get_items('megabox.vn',mode)
	elif query=='getstringsearch' or query=='dosearch':
		if query=='dosearch':string=name
		else:
			string=search_input_string('megabox.vn')
			if not string:return 'no'
		body=make_post(homepage+'search/autocomplete/?keyword=%s'%urllib.quote(string),resp='b')
		pattern='<a href="(http://phim.megabox.vn/.+?)".+?alt=\'(.+?)\' src="(.+?)"'
		for href,label,img in re.findall(pattern,body,re.DOTALL):
			addir_info(remove_tag(label),href,img,'',mode,1,'mgbplay')
	
	elif query=='mainpage':
		body=homehtml()
		if name==namecolor('Megabox gi???i thi???u'):
			content=xsearch('<ul class="hotFilmSlider">(.+?)</ul>',body,1,re.DOTALL)
			pattern="<a href='(http://phim.megabox.vn/.+?)'.+?src='(.+?)' alt='(.+?)'"
			for href,img,label in re.findall(pattern,content):
				addir_info(remove_tag(label),href,img,img,mode,1,'mgbplay')
		elif name==namecolor('Top 10 phim trong ng??y'):
			content=xsearch('<ul class="list topSlider">(.+?)end topFilm',body,1,re.DOTALL)
			pattern='href="(.+?)".+?<h3 class=\'H3title\'>(.+?)</h3>.+?src="(.+?)"'
			for href,label,img in re.findall(pattern,content,re.DOTALL):
				addir_info(remove_tag(label),href,img,'',mode,1,'mgbplay')
		elif 'xem nhi???u' in name:#l???-b???-show-clip xem nhi???u
			cats={'l???':1,'b???':2,'show':3,'clip':4};cat=[cats[s] for s in cats if s in name][0]
			link='http://phim.megabox.vn/mostviewed/ajax/?cat=%d&period=%d'
			period=['ng??y','tu???n','th??ng']#;per=[s[0] for s in period if s[0] in name][0]
			for i in range(1,4):
				add_sep_item(re.sub('\[.+?\]','',name)+' '+period[i-1])
				body=make_request(link%(cat,i))
				for b in re.findall('<li class="item">(.+?)</li>',body,re.DOTALL):
					href=xsearch('href="(.+?)"',b)
					img=xsearch('src="(.+?)"',b)
					title=xsearch("alt='(.+?)'",b).replace('Phim ','')
					tm=thuyetminh(b)+phim18(b)
					views=xsearch('</i>(.+?)</span>',b)
					if 'phim l???' in name:query='mgbplay';isFolder=False
					else:title=namecolor(title);query='1episode';isFolder=True
					title=tm+title+' %sviews: %s[/COLOR]'%(color['subscene'],views)
					addir(title,href,img,'',mode,1,query,isFolder)
		elif [s for s in ('Phim L???','Phim B???','Chi???u R???p') if s in name]:
			temp='Phim L??? M???i Nh???t' if 'L???' in name else 'Phim B??? M???i Nh???t' if 'B???' in name else 'Phim Chi???u R???p'
			content=xsearch('>%s</a>(.+?)>Xem th??m</a>'%temp,body,1,re.DOTALL)
			patt="href='(.+?)'.+?title.>(.+?)</h3>(.+?)<img.+?src='(.+?)'(.+?)</a>.+?<a.+?a>(.+?)</div></div>"
			put_items(re.findall(patt,content),'i')
		
	elif query=='MGB':
		dict=json_rw('megabox.json')
		if not dict.get('MGB1'):dict=update_dict(dict)
		name=color['search']+"Search tr??n megabox.vn[/COLOR]"
		addir(name,'megabox.vn',icon['megabox'],'',mode,1,'megabox.vn',True)
		for href,name in dict['MGB1']:#(phim-le,Phim l???),(phim-bo,Phim b???),(show,Show),(clip,Clip)
			addir(color['megabox']+name+'[/COLOR]',href,icon['megabox'],'',mode,1,'mainmenu',True)
		for name in dict['MGB2']:
			if isinstance(name,unicode):name=name.encode('utf-8')
			result=re.search('href="(.+?)">(.+?)</a>',name)
			if result:#L??? B??? Show Clip M???i Nh???t, Chi???u R???p
				title=namecolor(result.group(2));href=result.group(1)
				addir(title,href,icon['megabox'],'',mode,1,'subCate',True)
			else:#Megabox gi???i thi???u, Top 10, s???p chi???u, l???-b???-show-clip xem nhi???u
				title=namecolor(re.sub('<.+?>','',name+' trong ng??y' if 'xem' in name else name))
				addir(title,homepage,icon['megabox'],'',mode,1,'xemnhieu',True)
		if checkupdate('megabox.json',8):dict=update_dict(dict)
	
	elif query=='megabox.vn':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return megabox(query,url,img,fanart,mode,page,query)
		else:return 'no'
	elif query==name:#Search in megabox.vn
		search_string = urllib.quote_plus(query)
		body=make_post('http://phim.megabox.vn/tim-kiem?keyword=%s'%search_string).body
		body=sub_body(body,'class="item"','id="footer"')
		patt='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)"(.+?)</a>.+?<a.+?a>(.+?)</div></div>'
		put_items(re.findall(patt,body,re.DOTALL))
	
	elif query=='mainmenu' and url in ('phim-letl','phim-leqg','phim-botl','phim-boqg','showtl','showqg','cliptl'):
		dict=json_rw('megabox.json')
		if not dict.get(url):dict=update_dict(dict)
		for title,href in dict[url]:
			title=color['megabox']+title.replace('Phim ','')+'[/COLOR]'
			addir(title,href,icon['megabox'],'',mode,1,'mainmenu',True)
	
	elif query=='mainmenu':#url:(phim-le,phim-bo,show,clip)
		label=os.path.basename(url)
		submenu={'phim-le':'Phim l???','phim-bo':'Phim b???','show':'Show','clip':'Clip'}
		if label=='clip':
			title=color['xshare']+submenu[label]+' theo th??? lo???i[/COLOR]'
			addir(title,label+'tl',icon['megabox'],'',mode,1,query,True)
		elif label in ('phim-le','phim-bo','show'):
			title=color['xshare']+submenu[label]+' theo th??? lo???i[/COLOR]'
			addir(title,label+'tl',icon['megabox'],'',mode,1,query,True)
			title=color['xshare']+submenu[label]+' theo qu???c gia[/COLOR]'
			addir(title,label+'qg',icon['megabox'],'',mode,1,query,True)
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		body=sub_body(make_request(homepage+url,maxr=3),'begin primary','end primary')
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL),'i')
		url_next=xsearch('<li class="next"><a href="(.+?)">',body)
		if url_next:
			page_end=xsearch('<span></span>Trang.{1,10}/(\d{1,3})</div>',body)
			page_next=xsearch('trang-(.+)\Z',url_next)
			name=color['trangtiep']+'Trang ti???p theo: trang %s/%s[/COLOR]'%(page_next,page_end)
			addir(name,url_next,icon['megabox'],'',mode,1,query,True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	
	elif query=='mgbplay':
		url='/'.join((os.path.dirname(url),urllib.quote(os.path.basename(url))))
		body=make_request(url,resp='o',maxr=5);link=xsearch("changeStreamUrl\('(.+?)'\)",body.body)
		if not link:play_youtube(xsearch("\'(https://www.youtube.com/watch\?v=.+?)\'",body.body));return
		hd['Cookie']=body.cookiestring;href='http://phim.megabox.vn/content/get_link_video_lab'
		maxspeedlink=make_post(href,{'Referer':url},data={"link":"%s"%link},resp='j')
		if maxspeedlink.get('link'):
			name=re.sub(' \[COLOR.+?/COLOR\]','',name)
			xbmcsetResolvedUrl(maxspeedlink.get('link')+'|'+urllib.urlencode(hd),name+'Maxlink')
		else:mess('Get maxspeed link th???t b???i!','megabox.vn')
	
	elif 'episode' in query:
		art=fanart.split('/banner/')[0] if fanart!=fanart.split('/banner/')[0] else ''
		href=os.path.dirname(url);id=get_id(url)
		start=query.split('episode')[0];eps=query.split('episode')[1]
		#print 'http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start)
		j=make_request('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%s'%(id,start),resp='j')
		if j==False:addir(name.replace('orangered','grey'),url,img,'',mode,1,'mgbplay');return
		for epi in j:
			name=epi['name'];href='%s/%s-%s.html'%(href,epi['cat_id'],epi['content_id'])
			if not art:fanart='http://img.phim.megabox.vn/300x168'+epi['image_banner']
			else:fanart=art+epi['image_banner']
			addir(name,href,img,fanart,mode,1,'mgbplay')
		
		if make_request('http://phim.megabox.vn/content/ajax_episode?id=%s&start=%d'%(id,int(start)+30))!='false':
			name=color['trangtiep']+u'C??c t???p ti???p theo: %d-%s[/COLOR]'%(int(start)+30,eps)
			addir(name,url,img,fanart,mode,1,'%depisode%s'%(int(start)+30,eps),True)
	
	elif 'Megabox gi???i thi???u' in name:dict=json_rw('megabox.json');load_urls(dict['gioithieu'])
	elif 'Top 10 phim trong ng??y' in name:dict=json_rw('megabox.json');load_urls(dict['top10'])
	elif 'Phim s???p chi???u' in name:dict=json_rw('megabox.json');load_urls(dict['sapchieu'])
	elif query=='xemnhieu':#l???-b???-show-clip xem nhi???u
		cats={'l???':1,'b???':2,'show':3,'clip':4};cat=[cats[s] for s in cats if s in name][0]
		href='http://phim.megabox.vn/mostviewed/ajax/?cat=%d&period=%d'
		period=[('ng??y',1),('tu???n',2),('th??ng',3)];per=[s[0] for s in period if s[0] in name][0]
		for pe in period:
			if pe[0]==per:href=href%(cat,pe[1]);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name).replace(per,pe[0])+'[/COLOR]'
			addir(title,url,icon['megabox'],'',mode,1,query,True)
		load_urls(re.findall('<a href="(.+?)">',make_request(href,hd)))
	
	elif 'Phim Chi???u R???p' in name or query=='phim-chieu-rap':
		href='http://phim.megabox.vn/t/phim-chieu-rap-29/phim-le/trang-%d'
		body=sub_body(make_request(href%page,maxr=3),'begin main','end main')
		pattern='<a class.+?href="(.+?)".+?title.>(.+?)</h3>(.+?)<img.+?src="(.+?)">(.+?)</a>.+?<a.+?a>(.+?)</div><'
		href_new,dict=put_items(re.findall(pattern,body,re.DOTALL))
		page_end=xsearch('<li class="last"><a href="t/phim-chieu-rap-29/phim-le/trang-(.+?)">',body)
		name=color['trangtiep']+'Trang ti???p theo: trang %d/%s[/COLOR]'%(page+1,page_end)
		addir(name,href,icon['megabox'],'',mode,page+1,'phim-chieu-rap',True)
		if href_new:endxbmc();update_href_new(href_new,dict)
	
	elif query=='subCate':#url=phim-le,phim-bo,t/phim-chieu-rap-29,show,clip
		if '/' in url:gen=url.split('/')[1];url=url.split('/')[0]
		else:gen='ALL'
		cat={'phim-le':('L???',1),'phim-bo':('B???',2),'show':('Show',3),'clip':('Clip',4)}
		href='http://phim.megabox.vn/home/getcontent/?cat=%s&genre=%s&country=%s';dict=json_rw('megabox.json')
		for genre,country,gen_name in dict['subCate%d'%cat[url][1]]:
			#gen_name=gen_name.encode('utf-8') if type(gen_name)==unicode else s2u(gen_name)
			gen_name=u2s(gen_name)
			if gen_name==gen:href=href%(cat[url][1],genre,country);continue
			title=color['xshare']+re.sub('\[.?COLOR.*?\]','',name);
			title=re.sub('%s.+\Z'%cat[url][0],cat[url][0]+' %s M???i Nh???t[/COLOR]'%gen_name,title)
			addir(title,url+'/'+gen_name,icon['megabox'],'',mode,1,query,True)
		patt="<a class.+?href='(.+?)'.+?title.>(.+?)</h3>(.+?)<img.+?src='(.+?)'(.+?)</a>.+?<a.+?a>(.+?)</div></div>"
		put_items(re.findall(patt,make_request(href,hd),re.DOTALL),'i')
		cat={'phim-le':'Phim l???','phim-bo':'Phim b???','show':'Show','clip':'Clip'}
		name=color['trangtiep']+'%s Xem Th??m...[/COLOR]'%cat[url]
		addir(name,url,icon['megabox'],'',mode,1,'mainmenu',True)
	return ''

def get_home_page(fn,url='',update=False,hd=hd):
	def make_cookie_file(url,cookie):
		if 'vaphim.com' in url:makerequest(joinpath(xsharefolder,'vaphim.cookie'),cookie,'w')
		elif fn=='hayhaytv.html':makerequest(joinpath(xsharefolder,'hayhaytv.cookie'),cookie,'w')
			
	fullfilename=joinpath(xsharefolder,fn);body=''
	if not update and os.path.isfile(fullfilename):body=makerequest(joinpath(xsharefolder,fn))
	elif not update and url:
		response=make_request(url,hd,resp='o')
		if response:
			body=response.body;content=makerequest(fullfilename,re.sub('<script.+?/script>','',body),'w')
			if response.cookiestring:make_cookie_file(url,response.cookiestring)
	elif update and url and checkupdate(fn,folder=xsharefolder):
		response=make_request(url,hd,resp='o')
		if response:
			endxbmc();body=response.body;content=makerequest(fullfilename,re.sub('<script.+?/script>','',body),'w')
			if response.cookiestring:make_cookie_file(url,response.cookiestring)
	return body

def fptplay(name,url,img,mode,page,query):
	ico=icon['fptplay'];c=xsearch('([a-z]+)',color['fptplay'])
	
	def login():
		email=myaddon.getSetting('mail_fptplay');password=myaddon.getSetting('pass_fptplay')
		if not email:
			email,password=urllib2.base64.b64decode('eHNoYXJlQHRoYW5odGhhaS5uZXQ6YWRkb254c2hhcmU=').split(':')
		response=make_request('https://fptplay.net/tai-khoan',resp='o');hd['Cookie']=response.cookiestring
		response=make_post('https://fptplay.net/user/login',headers=hd,data={'email':email,'password':password})
		if 'state=fail' not in response.headers.get('location'):
			mess(u'Login th??nh c??ng','fptplay.net');hd['Cookie']=f=response.cookiestring
			response=make_request('https://fptplay.net/tai-khoan',hd,resp='o')
			f=f+':'+xsearch('name="_token".+?content="(.+?)"',response.body)
			makerequest(joinpath(xsharefolder,'fptplay.cookie'),f,'w')
		else:mess(u'Login kh??ng th??nh c??ng!','fptplay.net');f=': '
		return f
	
	def faddir(i):
		for title,href,img,dir in i:
			if not title:continue
			if dir:addir_info(namecolor(title,c),href,img,img,mode,1,'eps',True)
			else:addir_info(title,href,img,img,mode,1,'eps',True)
	
	def stream(href,id,epi='1'):
		data=urllib.urlencode({'id':id,'type':'newchannel','quality':'3','episode':epi,'mobile':'web'})
		try:link=json.loads(xread(href,hd,data)).get('stream');xbmcsetResolvedUrl(link)
		except:
			b=xread(url);id=xsearch("var id = '(.+?)'",b)
			data=urllib.urlencode({'id':id,'type':'newchannel','quality':'3','episode':epi,'mobile':'web'})
			href='https://fptplay.net/show/getlinklivetv'#cac link tv tren muc phim dang phat
			try:link=json.loads(xread(href,hd,data)).get('stream');xbmcsetResolvedUrl(link)
			except:pass
			print href,hd,data
	
	from resources.lib.servers import fptPlay;fpt=fptPlay()
	hd=fpt.hd
	
	if query=="fptplay.net":
		b=get_home_page('fptplay.html','https://fptplay.net')
		title=color['search']+"Search tr??n fptplay.net[/COLOR]"
		addir_info(title,'fptplay.net',ico,'',mode,1,'search',True)
		
		subbody=xsearch('(<ul class="top_menu">.+?</ul>)',b,1,re.DOTALL)
		for href,title in re.findall('<a href="(https://fptplay.net/[^"]+?)">(.+?)</a>',subbody):
			title=re.sub('<.+?>','',title)
			addir_info(namecolor(title,c),href,ico,'',mode,1,"category",True)
			
		add_sep_item('FPT Play gi???i thi???u -----------------------------------------')
		s=xsearch('(<ul class="slide_banner".+?/ul>)',b,1,re.S)
		faddir([fpt.detail(i) for i in re.findall('(<li.+?/li>)',s,re.S)])
		
		j='class="box_header Regular" href="javascript:void(0)"'
		for s in [i for i in re.findall('(<section>.+?</section>)',b,re.S) if j in i]:
			i=xsearch('<span class="pull-left">(.+?)</span>',s)
			add_sep_item('%s -----------------------------------------'%fpt.fpt2s(i))
			faddir([fpt.detail(i) for i in re.findall('(<li class="slide_img enyo".+?/li>)',s,re.S)])
		
		if get_home_page('fptplay.html','https://fptplay.net',True):xbmc.executebuiltin("Container.Refresh")
		if checkupdate('fptplay.cookie',30,xsharefolder):login()
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP" or url=="fptplay.net":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query.strip():return
		elif 'Page next:' not in name:page=1
		
		b=xread('https://fptplay.net/tim-kiem/%s'%urllib.quote(query))
		faddir([fpt.detail(i) for i in b.split('list_img') if '<div class="title">' in i])
		
		pn=xsearch('id="paging_(.+?)_',b)
		if pn:
			pn='type=search&stucture_id=search&page=2&keyword='+query
			addir_info('[COLOR lime]Page next: %d[/COLOR]'%(page+1),pn,ico,'',mode,page+1,"pageNext",True)
	
	elif url=='https://fptplay.net/livetv':
		for title,href,img in fpt.liveChannals():
			if 'sep' in href:add_sep_item('%s -----------------------------------------'%title)
			else:addir_info(namecolor(title,c),os.path.basename(href),img,'',mode,1,'playTV')
			
	elif query=='playTV':#stream('https://fptplay.net/show/getlinklivetv',url)
		link=fpt.liveLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('Get channel link fail!') 
	
	elif query=='category':
		b=xread(url)
		i=re.findall('<a class="box_header Regular" href="(.+?)"><span class="pull-left">(.+?)</span></a>',b)
		if not i:return fptplay(name,url,img,mode,page,'page')
		for href,title in i:
			addir_info(namecolor(fpt.fpt2s(title),c),href,ico,'',mode,1,"page",True)
		
		add_sep_item('FPT Play gi???i thi???u -----------------------------------------')
		faddir([fpt.detail(i) for i in re.findall('(<li class="banner".+?/li>)',b,re.S)])
				
	elif query=='page':
		b=xread(url)
		faddir([fpt.detail(i) for i in b.split('list_img') if '<div class="title">' in i])
		
		pn=xsearch('id="paging_(.+?)_',b)
		if pn:
			pn='type=new&stucture_id=%s&page=2'%pn
			addir_info('[COLOR lime]Page next: %d[/COLOR]'%(page+1),pn,ico,'',mode,page+1,"pageNext",True)
	
	elif query=='pageNext':
		b=xread('https://fptplay.net/show/more',hd,url)
		s=[i for i in b.split('list_img') if '<div class="title">' in i]
		faddir([fpt.detail(i) for i in s])
		
		if len(s)==30:
			url=re.sub('page=\d+','page=%d'%(page+1),url)
			addir_info('[COLOR lime]Page next: %d[/COLOR]'%(page+1),url,ico,'',mode,page+1,"pageNext",True)
	
	elif query=='eps':
		items=fpt.eps(url,page)
		for title,href in items:
			if 'C??c t???p ti???p theo' in title:addir_info(title,url,ico,'',mode,page+1,"eps",True)
			else:addir_info(title,href,img,img,mode,1,'play')
		#if not items:addir_info(namecolor(name),xsearch('(\w{20,30})',url),img,img,mode,1,'play')
		if not items:addir_info(namecolor(name),url,img,img,mode,1,'play')
	
	elif query=='play':
		if '?' not in url:stream('https://fptplay.net/show/getlink',url)
		else :stream('https://fptplay.net/show/getlink',url.split('?')[0],url.split('?')[1])

def dangcaphd(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phim3s.png');homepage='http://dangcaphd.com/movie/movies.html'
	
	def namecolor(name):return '%s%s[/COLOR]'%(color['dangcaphd'],name)
	def dangcaphd_get_link(url,loop=True):
		hd['Cookie']=makerequest(joinpath(xsharefolder,'dchd.cookie'))
		body=make_request(url.replace('/movie-','/watch-'),headers=hd)
		if not body or re.search('class="f20 mb10"',body):
			if loop:login();dangcaphd_get_link(url,loop=False)
			else:mess(u'Hi???n t???i - B???n ch??? c?? th??? xem b???n Demo c???a dangcaphd.com','dangcaphd.com')
		return re.findall('"(\d{,3})" _link="(.+?)" _sub="(.*?)"',body)
	
	def dangcaphd_download_sub(url):
		if myaddon.getSetting('autodel_sub')=='true':delete_files(subsfolder)
		subfullpathfilename=joinpath(subsfolder,'vie.%s'%os.path.basename(url));sub=''
		if os.path.splitext(subfullpathfilename)[1] in [".srt", ".sub", ".txt", ".smi", ".ssa", ".ass"]:
			if makerequest(subfullpathfilename,make_request(url),'wb'):sub=subfullpathfilename
		return sub
		
	def dchd_dir(s):
		href=xsearch('href="(.+?)"',s)
		title=xsearch('title="(.+?)"',s)
		res=xsearch('"Ch???t l?????ng (.+?)"',s)
		if res:title=title+' [COLOR gold]%s[/COLOR]'%res
		img=xsearch('src="(.+?)"',s)
		eps=xsearch('class="bxitem-episodes"><span>(.+?)</span></span>',s).replace('<br>',' ')
		if eps:title=namecolor(title)+' - [COLOR green](%s)[/COLOR]'%eps;dir=True;query='episodes'
		else:dir=False;query='dchd_play'
		addir_info(title,href,img,'',mode,1,query,dir)
	
	def login():
		def input_captcha(tempfile):
			mywindow = xbmcgui.Window();image = xbmcgui.ControlImage(0, 0, 200,100,tempfile)
			mywindow.addControl(image);mywindow.show()
			captcha = get_input('????? login dangcaphd.com, h??y nh???p chu???i b???n nh??n th???y m??n h??nh')
			mywindow.close()
			return captcha
			
		url="http://dangcaphd.com/login.html";result='No'
		mail_dchd=myaddon.getSetting('mail_dchd');pass_dchd=myaddon.getSetting('pass_dchd')
		if not mail_dchd:
			mail_dchd='1@kodi.com';pass_dchd='123456'
			mess(u'B???n ??ang d??ng acc test c???a xshare!','xshare.vn');xbmc.sleep(5000)
		response=make_request(url,resp='o')
		if not response:return result
		hd['Cookie']=response.cookiestring
		captcha=xsearch('_captcha="(.+?)"',response.body)
		response=make_request(captcha,headers=hd)
		if not response:return result
		tempfile = joinpath(tempfolder,"temp.jpg");makerequest(tempfile,response,"wb")
		captcha=input_captcha(tempfile)
		data={'remember':'on', 'email':mail_dchd,'password': pass_dchd,'_submit': 'true','security_code':captcha}
		response=make_post(url,hd,data)
		if not response.cookies.get('user_password'):mess(u'Login kh??ng th??nh c??ng!','dangcaphd.com')
		else:
			mess(u'Login th??nh c??ng','dangcaphd.com')
			result='user_email=%s;user_password=%s'%(response.cookies.get('user_email'),response.cookies.get('user_password'))
			makerequest(joinpath(xsharefolder,'dchd.cookie'),result,'w')
			logout_site(result,'http://dangcaphd.com/logout.html')
		
		return result
	
	if query=='dangcaphd.com':
		body=get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html')
		name=color['search']+"Search tr??n dangcaphd.com[/COLOR]"
		addir(name,"dangcaphd.com",icon['dangcaphd'],mode=mode,query="search",isFolder=True)
		for i in ('Th??? lo???i','PHIM L???','PHIM B???','QU???C GIA','Xem nhi???u (t??? trang 2)','Phim chi???u r???p'):
			addir_info(namecolor(i),'',ico,'',mode,1,i,True)
		add_sep_item('----------Xem nhi???u (trang 1)-----------')
		p='(<div class="tn-bxitem">.+?<div class="tn-contentdecs mb10">)'
		for s in re.findall(p,body,re.DOTALL):dchd_dir(s)
		
		if get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html',True):
			xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return dangcaphd(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="dangcaphd.com":
		search_string = urllib.quote_plus(query)
		url='http://dangcaphd.com/movie/search.html?key=%s&search_movie=1'%search_string
		return dangcaphd(name,url,img,mode,1,query='page')
	
	elif query=='Th??? lo???i':
		body=get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html')
		for href,name in re.findall('<a href="(http://dangcaphd.com/cat.+?)" title="(.+?)">',body):
			addir_info(namecolor(name),href,ico,'',mode,1,'page',True)
		
	elif query=='QU???C GIA':
		body=get_home_page('dchd.html','http://dangcaphd.com/movie/top_view.html')
		for href,name in re.findall('<a href="(http://dangcaphd.com/country.+?)" title="(.+?)">',body):
			addir_info(namecolor(name),href,ico,'',mode,1,'page',True)
	
	elif query in ('page','PHIM L???','PHIM B???','Xem nhi???u (t??? trang 2)','Phim chi???u r???p'):
		if query =='PHIM L???':url='http://dangcaphd.com/movie/movies.html'
		elif query =='PHIM B???':url='http://dangcaphd.com/movie/series.html'
		elif query =='Xem nhi???u (t??? trang 2)':url='http://dangcaphd.com/movie/top_view.html?&per_page=35';page=2
		elif query =='Phim chi???u r???p':url='http://dangcaphd.com/movie/cinema.html'
		body=make_request(url)
		S=xsearch('<div class="tn-main-full">(.+?)<footer class="tn-footer-full">',body,1,re.DOTALL)
		for s in re.findall('(<li class=.+?</strong></span>)',S,re.DOTALL):dchd_dir(s)
			
		pn=xsearch('<a href="([^<]+?)">&gt;</a>',S).replace('amp;','')
		if pn:
			pl=xsearch('page=(\d+?)">&gt;&gt;</a>',S)
			pl=str(int(pl)/35) if pl else ''
			title=color['trangtiep']+'Trang ti???p theo: trang %d/%s[/COLOR]'%(page+1,pl)
			addir_info(title,pn,ico,'',mode,page+1,'page',True)
		
	elif query=='episodes':
		for epi,href,sub in dangcaphd_get_link(url):
			href=href.replace(' ','%20').strip()+'xshare'+sub.replace(' ','%20').strip()
			title='T???p %s - '%epi+re.sub(' - \(.+?\)','',re.sub('\[/?COLOR.*?\]','',name))
			addir_info(title,href,img,'',mode,1,'dchd_play')
		
	elif query=='dchd_play':
		subtitle=''
		if os.path.splitext(url)[1].lower()=='.html':
			links=dangcaphd_get_link(url)
			url=links[0][1].replace(' ','%20').strip()
			if links[0][2]:subtitle=dangcaphd_download_sub(links[0][2].strip())
		else:
			if url.split('xshare')[1]:subtitle=dangcaphd_download_sub(url.split('xshare')[1])
			url=url.split('xshare')[0]
		if subtitle:
			xbmcsetResolvedUrl(url,urllib.unquote(os.path.splitext(os.path.basename(subtitle))[0]))
			mess(u'Ph??? ????? c???a dangcaphd.com','dangcaphd.com')
		else:xbmcsetResolvedUrl(url)
		
def vuahd(name,url,img,fanart,mode,page,query):
	col='[COLOR tomato]';ico=os.path.join(iconpath,'vuahd.png');urlhome='http://vuahd.tv/'
	def namecolor(name):return '%s%s[/COLOR]'%(col,name)
	def vuahd_login(headers=''):
		if not headers:
			url='http://vuahd.tv/accounts/login'
			response=make_request(url,resp='o');hd['Cookie']=response.cookiestring
			t=xsearch("name='csrfmiddlewaretoken' value='(.+?)'",response.body)
			u=myaddon.getSetting('usernamev');p=myaddon.getSetting('passwordv')
			data=urllib.urlencode({'csrfmiddlewaretoken':t,'username':u,'password':p})
			response=make_post(url,hd,data)
			if response.status==302:
				f=response.cookiestring;hd['Cookie']=f
				if re.search('<b>Free</b></span>',make_request('http://vuahd.tv/accounts/profile/',headers=hd)):
					mess(u'T??i kho???n free ch??? xem ???????c m???t s??? phim.','vuahd.tv')
				else:mess(u'Login th??nh c??ng','vuahd.tv')
				makerequest(joinpath(xsharefolder,'vuahd.cookie'),f,'w')
			else:mess(u'Login kh??ng th??nh c??ng!','vuahd.tv');f=''
			return f
		else:make_request('http://vuahd.tv/accounts/logout',headers=headers)
	def readpage(url,items=list()):
		hd['Cookie']=makerequest(joinpath(xsharefolder,'vuahd.cookie'))
		for detail in re.findall('<div class="item-film">(.+?)</p>',make_request(url,hd),re.DOTALL):
			name=xsearch('title="(.+?)"',detail);href=urlhome+xsearch('href="(.+?)"',detail)
			img=urlhome+xsearch('src="(.+?)"',detail);isFolder='/tv-series/' in href
			items.append((name,href,img,isFolder))
		return items
	def vuahd_addir(items):#title,href,img,isFolder
		for title,href,img,isFolder in items:
			if isFolder:title=namecolor(title);query='vuahdfolder'
			else:query='vuahdplay'
			addir_info(title,href,img,'',mode,1,query,isFolder)
	
	if query=='vuahd.tv':
		body=makerequest(joinpath(xsharefolder,'vuahd.html'))
		name=color['search']+"Search tr??n vuahd.tv[/COLOR]"
		addir_info(namecolor(name),'',icon['isearch'],'',mode,1,'vuahdsearch',True)
		for title in re.findall(' <li class="active has-child"><a href="/" title=".+?">(.+?)</a>',body):
			addir_info(namecolor(title),'',ico,'',mode,1,'submenu',True)
		vuahd_addir(readpage('http://vuahd.tv/movies/all-items?page=1'))
		name='%sT???t c??? phim: trang 2[/COLOR]'%color['trangtiep']
		addir_info(name,'http://vuahd.tv/movies/all-items?page=',ico,'',mode,1,'vuahdpage',True)
		if checkupdate('vuahd.html',8,xsharefolder):
			endxbmc();body=make_request('http://vuahd.tv/',hd)
			if len(body)==0:hd['Cookie']=vuahd_login();body=make_request('http://vuahd.tv/',hd)
			makerequest(joinpath(xsharefolder,'vuahd.html'),body,'w')
	elif query=='submenu':
		body=makerequest(joinpath(xsharefolder,'vuahd.html'))
		name=re.sub('\[/?COLOR.*?\]','',name)
		detail=xsearch(' <li[^/]+?><a href="/" title="[^/]+?">%s</a>(.+?)</ul>'%name,body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)".*?>(.+?)</a>',detail):
			addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'vuahdpage',True)
		if 'Th??? lo???i' in name:
			for href,title in [('51','Phim B??? Trung Qu???c'),('52','Phim B??? H??n Qu???c'),('53','Phim B??? B??? Anh-M???'),('56','Phim B??? Kh??c')]:
				addir_info(namecolor(title),'%s/movies/tv-series/%s/'%(urlhome,href),ico,'',mode,1,'vuahdpage',True)
	elif query=='vuahdpage':
		name=re.sub('\[/?COLOR.*?\]','',name).split(':')[0]
		if 'page=' not in url:
			if 'trailers' in url:url='http://vuahd.tv/movies/all-trailers?page='
			elif url=='http://vuahd.tv/movies/':url='http://vuahd.tv/movies/all-items?page='
			elif url=='http://vuahd.tv//movies/':url='http://vuahd.tv/movies/all-items?page='
			elif '/tv-series/' in url:url=url.replace('tv-series','tv-series-items')+'?page='
			else:url=url+'items?page='
		items=readpage(url+str(page));vuahd_addir(items)
		if items:
			name='%s%s: trang %d[/COLOR]'%(color['trangtiep'],name,page+1)
			addir_info(name,url,ico,'',mode,page+1,'vuahdpage',True)
	elif query=='vuahdfolder':
		hd['Cookie']=makerequest(joinpath(xsharefolder,'vuahd.cookie'));body=make_request(url,hd)
		head=xsearch('\((.+?)\(',xsearch('<header(.+?)header>',body,1,re.DOTALL))
		if head:head=' - '+head.strip()
		items=sets(re.findall('<a href="(.+?)" class="btn-1">Xem (.+?)</a>',body))
		items=[s for s in items if 'title=' not in s[0]]
		for href,label in items:
			title=label.strip()+'/%s - '%xsearch('\(\d{1,4}/(\d{1,4})\)',name)+remove_tag(name)+head
			addir_info(title,urlhome+href,img,fanart,mode,page,'vuahdplay')
	elif query=='vuahdplay':#xhr.setRequestHeader("X-CSRFToken", csrftoken);
		hd['Cookie']=vuahd_login();body=make_request(url+('/watch' if '/watch' not in url else ''),hd)
		href=xsearch('<source src = "(.+?)"',body)
		if not href:href=xsearch('file: "(.+?)"',body)
		if href:xbmcsetResolvedUrl(urlhome+href)#vuahd_login(hd)
		else:mess(u'Kh??ng get ???????c maxspeed link!','vuahd.tv')

def pubvn(name,url,img,mode,page,query):
	color['pubvn']='[COLOR deepskyblue]';icon['pubvn']=os.path.join(iconpath,'pubvn.png');homepage='http://pubvn.tv/'
	txtfile=joinpath(xsharefolder,'pubvn'+datetime.date.today().strftime("%d")+'.txt')
	def login():
		u=myaddon.getSetting('usernamep');p=myaddon.getSetting('passwordp')
		data='txtusername=%s&txtpass=%s&remeber_me1=0&sercurity_code='%(u,p)
		response=make_post(homepage+'phim/aj/action_login.php',data=data)
		if 'pub_userid=deleted' in response.cookiestring:mess(u'Login kh??ng th??nh c??ng!','pub.vn')
		else:mess(u'Login th??nh c??ng','pub.vn')
		return {'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0','Cookie':response.cookiestring}
	def getiMovEps(url):
		hd=login();pattern='<input id="thread_id" type="hidden" value="(.+?)"/>'
		thread_id=xsearch(pattern,make_request(url));pattern='id="player" src="(.+?)"'
		iMovEps=xsearch(pattern,make_request(homepage+'/bar/dodamde/'+thread_id,headers=hd))
		return homepage+iMovEps,hd
	def pubvn_play(url):
		if '=' not in url:url,hd=getiMovEps(url)
		else:hd=login()
		body=make_request(url+'&server=3',headers=hd)
		id=re.search('iMov=(\d{4,6})&iEps=(\d{5,7})',url);mov_id=id.group(1);eps_id=id.group(2)
		log_id=xsearch('log_id : (\d{5,7})',body)
		pub_id=xsearch('pub_id : "(.+?)"',body)
		lte_id=xsearch('lte_id : (\w{6,10})',body)
		sercur=xsearch('sercur : (\w{6,10})',body)
		hash=xsearch("hash : '(\w{8,10})'",body)
		dlink=xsearch("file: '(.+?)'",body)
		data='action=update_last_watched&user_id=%s&mov_id=%s&eps_id=%s&time=93.78&per=1&hash=%s'
		data=data%(log_id,mov_id,eps_id,hash)
		make_post(homepage+'movie/vn/vasi_blahblah.php',hd,data)
		make_request(homepage+'phim/logout.php',headers=hd);xbmcsetResolvedUrl(dlink+'?start=0')
	def pubvn_Eps(url):
		body=make_request(url+'&server=3');temp=[];items=[]
		epslist=re.findall('{"ver_id":(.+?),"ver_name":"(.+?)","eps_list":(\[.+?\])}',body,re.DOTALL)
		for ver_id,ver_name,eps_list in epslist:
			if ver_name not in temp:
				temp.append(ver_name)
				try:
					for eps in eval(re.sub('true|false','""',eps_list)):
						href='%s=%s=%d'%(url.split('=')[0],url.split('=')[1],eps['id'])
						name=eps['name']+'-'+ver_name.strip() if len(epslist)>2 else eps['name']
						items.append((name,href))
				except:pass
		return items
	def pubvn_page(body,items=[]):
		pattern='</p></a>(.+?)<a href=".+?">.{,20}<img src="(.+?)".{,200}<a href="(.+?)" title="(.+?)">'
		for eps,img,href,title in re.findall(pattern,body,re.DOTALL):
			eps=xsearch('<p>(\d{1,3}/\d{1,3})</p>',eps.strip()).split('/')[0]>'1'
			if eps:items.append(('%s%s[/COLOR]'%(color['pubvn'],title),homepage+href,img,'folder'))
			else:items.append((title,homepage+href,img,'play'))
		return items
	def pubvn_search(string,page=1):
		data='boxphim=Filter&txtsearch=%s&page=%d'%(urllib.quote_plus(string),page)
		body=make_post(homepage+'phim/aj/advancesearch.php',data=data).body
		for name,href,img,type in pubvn_page(body):
			addir(name,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xsearch('class="vpage(\d{1,4})".{,5}>Cu???i</a></li>',body).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=color['trangtiep']+'Trang ti???p theo: trang %s/%s[/COLOR]'%(str(page+1),trangcuoi)
			addir(name,url,img,fanart,mode,page=page+1,query=string,isFolder=True)
		return ''
	def pubvn_make_txt(items,temps=[]):
		for href,name,img in items:
			body=make_request(homepage+href)
			thread_id=xsearch('/bar/threads/(\d{3,6})',body)
			eps=xsearch('<p>(\d{1,3}/\d{1,3})</p>',body);page=0
			if eps.split('/')[0]>'1':page=1;name=color['pubvn']+name+'[/COLOR]'
			temps.append((name,homepage+'/bar/dodamde/'+thread_id,img,page))
		if temps:delete_files(data_path,mark='pubvn');makerequest(txtfile,str(temps),'w')
	if query=='pubvn.tv':
		name=color['search']+"Search tr??n pubvn.tv (pub.vn)[/COLOR]"
		addir(name,url,icon['icon'],mode=mode,query='search',isFolder=True)
		body=make_request(homepage+'phim/home.php')
		#blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for name in re.findall('<a class="Title_menu">(.+?)</a>',body):
			page+=1;name='%s%s[/COLOR]'%(color['pubvn'],name)
			addir(name,'Title_menu',img,fanart,mode,page,query='blmenu_childs',isFolder=True)
		body=body[body.find('Phim Hot'):body.find('<a>Phim l???</a>')]
		phimhots=re.findall('<a href="(.+?)" class=".+?" title="(.+?)\|.{,2000}src="(.+?)"',body,re.DOTALL)
		name='%sPhim HOT[/COLOR]'%color['pubvn']
		addir(name,'Phim_Hot',img,fanart,mode,page,query=query,isFolder=True)
		temp=[('Phim l???','32','126'),('Phim b??? ??u - M???','60-1','126-1'),('Phim b??? Ch??u ??','60-2','126-2')]
		for name,cat_id,type in temp:
			addir('%s%s[/COLOR]'%(color['pubvn'],name),'Home_Main',img,fanart,mode,page=1,query=cat_id,isFolder=True)
			if myaddon.getSetting('phim18')=="true":
				name='%s%s[/COLOR]'%(color['pubvn'],name+' - 18+')
				addir(name,'Home_Main',img,fanart,mode,page=1,query=type,isFolder=True)
		endxbmc();pubvn_make_txt(phimhots)
	elif query=='search':make_mySearch('',url,'','',mode,'get')
	elif query=="INP":pubvn_search(make_mySearch('',url,'','','','Input'))
	elif url=='pubvn.tv':page=1 if 'Trang ti???p theo' not in name else page;pubvn_search(query,page)
	elif url=='Title_menu':
		body=make_request(homepage+'phim/home.php')
		blmenu_childs=re.findall('<li><a menuid = "(.+?)" tabid="(.+?)">(.+?)</a></li>',body)
		for menuid,tabid,name in blmenu_childs:
			if int(tabid)==page:
				addir('%s%s[/COLOR]'%(color['pubvn'],name),'blmenu_child',img,fanart,mode,page,query=menuid,isFolder=True)
	elif url=='blmenu_child':
		data='tabid=%s&menuid=%s'%(str(page),query)
		body=make_post(homepage+'phim/aj/aj_top.php',data=data).body
		pattern='<div class="film_poster">(.+?)<a href="(.+?)" class="tooltip1" title="(.+?)\|.{,2000}src="(.+?)" (.{,500}End class = film_poster)'
		for s1,href,title,img,s2 in re.findall(pattern,body,re.DOTALL):
			s1=xsearch('<p>(\d{1,3}/\d{1,3})</p>',s1.strip()).split('/')[0]>'1'
			s2=xsearch('<p>(\d{1,3}/\d{1,3})</p>',s2.strip()).split('/')[0]>'1'
			if s1 or s2:addir('%s%s[/COLOR]'%(color['pubvn'],title),homepage+href,img,fanart,mode,page,query='folder',isFolder=True)
			else:addir(title,homepage+href,img,fanart,mode,page,query='play')
	elif query=='folder':
		url,hd=getiMovEps(url)
		for eps,href in pubvn_Eps(url):
			addir(eps+' - '+re.sub('\[.?COLOR.{,12}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Phim_Hot':
		if not os.path.isfile(txtfile):
			for file in os.listdir(xsharefolder):
				if 'pubvn' in file:txtfile=joinpath(xsharefolder,file);break
		try:items=eval(makerequest(txtfile))
		except:items=[]
		if items:
			for name,href,img,page in items:
				addir(name,href,img,fanart,mode,page=page,query='dodamde',isFolder=(page==1))
		else:mess(u'??ang c???p nh???t d??? li???u - ch???n l???i sau 30 gi??y n???a nh??...')
	elif query=='dodamde':
		iMovEps=xsearch('id="player" src="(.+?)"',make_request(url))
		if page==0:pubvn_play(homepage+iMovEps)
		else:
			for eps,href in pubvn_Eps(homepage+iMovEps):
				addir(eps+' - '+re.sub('\[.?COLOR.{,15}\]','',name),href,img,fanart,mode,page,query='play')
	elif url=='Home_Main':
		url=homepage+'phim/aj/';data='cat_id=%s&type=%s&page=%s'
		if 'Phim l???' in name:url+='aj_phimle.php';data='cat_id=%s&page=%s'%(query,str(page))
		else:url+='aj_series.php';data=data%(query.split('-')[0],query.split('-')[1],str(page))
		body=make_post(url,data=data).body
		for title,href,img,type in pubvn_page(body):
			addir(title,href,img,fanart,mode,page,query=type,isFolder=(type=='folder'))
		trangcuoi=xsearch('class="catpage(\d{1,4})".{,5}>Cu???i</a></li>',body).strip()
		if trangcuoi and int(trangcuoi)>page:
			name=re.sub('\[.?COLOR.{,12}\]','',name).split('*')[0].strip()
			name=color['trangtiep']+'%s * Trang ti???p theo: trang %s/%s[/COLOR]'%(name,str(page+1),trangcuoi)
			addir(name,'Home_Main',img,fanart,mode,page=page+1,query=query,isFolder=True)
	elif query=='play':pubvn_play(url)

def hdviet(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';ico=icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	urlhome='http://movies.hdviet.com/';c='darkorange'
	if os.path.isfile(joinpath(datapath,'hdviet.cookie')):os.remove(joinpath(datapath,'hdviet.cookie'))
	direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'
	
	def getcookie():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		return response.cookiestring
	
	def login_hdviet():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		try:resp=response.json#;print resp
		except:resp={u'r': u'L???i ????ng nh???p hdviet.com', u'e': 3}
		if resp.get('e')==0:
			mess(resp.get('r'),'hdviet.com');hd['Cookie']=response.cookiestring
			response=make_request('http://movies.hdviet.com/dieu-khoan-su-dung.html',headers=hd)
			import base64;token=base64.b64decode(xsearch('<a class="userinfo".+?token=(.+?)"',response))
			response={'Cookie':hd['Cookie'],'access_token':token};json_rw('hdviet.cookie',response)
		else:response=dict();mess(resp.get('r'),'hdviet.com')
		url='http://movies.hdviet.com/dang-xuat.html?accesstokenkey=%s'
		make_post(url%response.get('access_token')).body
		return response
	
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=')
			response=make_request(direct_link%(token,id_film),resp='j')
			try:links=response['r']
			except:links=dict()
			#try:print json.dumps(links,indent=2,ensure_ascii=True)
			#except:pass
			return links
		
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		if not link:return '',''
		elif '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		
		if link:
			max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			
			r=''.join([s for s in resolutions if s in link]);response=''
			if r:
				href=link[:link.rfind(r)]+link[link.rfind(r):].replace(r,'%s')
				for i in resolutions:
					if i>max_resolution:continue
					response=make_request(href%i)
					if len(response)>0:link=href%i;break
			else:
				href=link.replace('playlist.m3u8','playlist_h.m3u8')
				response=make_request(href)
				if not response or '#EXT' not in response:
					for s in range(1,6):
						#print re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href)
						if 'http://n0%d'%s in href:continue
						elif re.search('http://n0\d.vn-hd.com',href):
							response=make_request(re.sub('http://n0\d.vn-hd.com','http://n0%d.vn-hd.com'%s,href))
						if response and  '#EXT' in response:break
				if not response:response=make_request(link)
			
			if response and '#EXT' in response:
				items=re.findall('RESOLUTION=(\d+?)x.*\s(.+m3u8)',response)
				if items:
					res=0;hr=''
					for r,h in items:
						#print r,h
						if int(r)>res:res=int(r);hr=h
					if hr and 'http://' in hr:link=hr
					else:link=os.path.dirname(link)+'/'+hr
				else:
					items=re.findall('(.+m3u8)',response)
					if items and 'http://' in items[0]:link=items[len(items)-1]#;print items[0]
					elif items:link=os.path.dirname(link)+'/'+items[0]
				
			else:link=''
		if not link:return '',''
		audio=links.get('AudioExt',list());audioindex=-1;linksub=''
		if not audio:pass
		elif len(audio)>1:
			audio_choice=myaddon.getSetting('hdvietaudio')
			if audio_choice=='H???i khi xem':
				title=u'[COLOR green]Ch???n Audio[/COLOR]';line1= u'[COLOR yellow]Vui l??ng ch???n Audio[/COLOR]'
				audioindex=mess_yesno(title,line1,'',audio[0].get("Label",'0'),audio[1].get("Label",'1'))
			else:audioindex=0 if u2s(audio[0].get("Label")) in audio_choice else 1
			if 'Thuy???t' not in u2s(audio[audioindex].get("Label")):linksub='yes'#b???t c??? download sub
			try:link=link+'?audioindex=%d'%(int(audio[audioindex].get("Index",'0'))-1)
			except:pass
		elif u2s(audio[0].get("Label"))=='Thuy???t Minh':audioindex=0
		if audioindex<0 or linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:linksub=links[source]['VIE']['Source']
				except:linksub=''
				if linksub:break
		#print 'getResolvedUrl: %s - %s'%(link,linksub)
		return link,linksub

	def additems(body):
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail);title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			rat=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail)
			if not epi:title=TM+' '+title;query='hdvietplay'
			elif epi=='1':query='hdvietfolder'
			else:title=TM+' '+namecolor(title,c)+' [COLOR green](%s)[/COLOR]'%epi;query='hdvietfolder'
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=img)
			if rat:rat='[COLOR tomato]IMDb:[/COLOR] %s, '%rat
			if upl:upl='[COLOR tomato]Uploader:[/COLOR] %s, '%upl
			if act:act='[COLOR tomato]Di???nvi??n:[/COLOR] %s, '%act
			if drt:drt='[COLOR tomato]?????odi???n:[/COLOR] %s, '%drt
			plot=rat+upl+act+drt+'\n'+plot
			info={'title':title,'year':year,'rating':xsearch('(\d\.\d{1,2})',rat),'plot':plot,'episode':epi,'director':drt,'writer':act}
			listItem.setInfo(type="Video", infoLabels=info)
			listItem.setArt({"thumb":img,"poster":img,"fanart":img})
			if query=='hdvietplay':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+id_film+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(img)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+urllib.quote_plus(title)
			listitems.append((u,listItem,False if query=='hdvietplay' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
	
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote_plus(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	
	if query=='hdviet.com':
		body=get_home_page('hdviet.html',urlhome)
		name=color['search']+"Search tr??n hdviet.com[/COLOR] (H??y ch???n ????? ph??n gi???i tr??n settings nh??)"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',ico,fanart,mode,1,'search',True)
		href='http://movies.hdviet.com/phim-yeu-thich.html'
		title=color['search']+'Phim y??u th??ch c???a t??i tr??n hdviet[/COLOR]'
		addir_info(title,href,icon['icon'],fanart,mode,1,'yeu-thich',True)
		
		
		items=re.findall('class="mainmenulist.+?href="(.+?)".+?title=.+?>(.+?)</a>',body,re.DOTALL)
		for href,name in items:
			addir_info(namecolor(name,c),href,ico,fanart,mode,1,'mainmenulist',True)
		
		items=re.findall('<div class="h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>.+?</div>(.+?)</ul>',body,re.DOTALL)
		for href,name,subbody in items:
			addir('-----%s%s-----[/COLOR]'%(color['search'],name),href,icon['hdviet'],fanart,mode,page,'1',True)
			additems(subbody)
		if get_home_page('hdviet.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=='mainmenulist':
		body=get_home_page('hdviet.html',urlhome)
		if 'phim-le' in url:
			s=xsearch('(id="menu-phimle".+?</ul>)',body,1,re.DOTALL)
			for href,title in re.findall('href="(.+?)".+?>([^<]+?)</a>',s):
				addir_info(namecolor(title,c),href,ico,'',mode,1,'else',True)
		elif 'phim-bo' in url:
			s=xsearch('(id="menu-phimbo".+?"mainmenulist fause")',body,1,re.DOTALL).replace('\n','')
			link=name='xshare'
			for href,title in re.findall('href="(.+?)".+?>([^<]+?)</a>',s):
				title=' '.join(s for s in title.split())
				if link!='http://movies.hdviet.com/phim-bo.html' and link.replace('.html','') in href:title=name+' - '+title
				else:link=href;name=title
				addir_info(namecolor(title,c),href,ico,'',mode,1,'else',True)
	
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif url=='hdviet.com' or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return
		
		page=1 if 'Trang ti???p theo' not in name else page
		b=xread('http://movies.hdviet.com/tim-kiem-nhanh.html?keyword=%s'%urllib.quote_plus(query))
		try:j=json.loads(b).get('Title')
		except:j={}
		if j:
			add_sep_item('-------K???t qu??? t??m nhanh------')
			for i in j:
				i=j.get(i);href=i.get('MovieID');img=i.get('Backdrop').replace(' ','')
				title=namecolor(u2s(i.get('KnownAs')+' - '+i.get('MovieName')),c)
				addir_info(title,href,img,img,mode,1,"hdvietfolder",True)
		
		b=xread('http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote(query))
		add_sep_item('-------%s------'%re.sub('<[^<]+>','',xsearch('<h1 class="h2-ttlpage2">(.+?)</h1>',b)))
		additems(xsearch('("cf box-movie-list box-movie-list-search".+?<div class="box-ribbon mt-15">)',b,1,re.DOTALL))
		s=xsearch('(<ul class="paginglist paginglist-center">.+?</ul>)',b,1,re.DOTALL)
		i=re.search('"active"[^"]+""><a href="([^"]+)">(\d+)</a>',s)
		if s:
			un=i.group(1);pn=i.group(2);pages=xsearch('>(\d+)</a></li></ul>',s)
			title='%sTrang ti???p theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pn,pages)
			addir(title,un,img,fanart,mode,page,'else',True)
			
		
		for s in [i for i in b.split('<div class="box-ribbon mt-15">') if '<div class="h2-ttl cf">' in i]:
			i=re.search('<h2 class="h2-ttlin fl-left"><a href="([^"]+)" title="([^"]+)"',s)
			if i:addir_info(namecolor('-------%s Xem T???t C???------'%i.group(2),'lime'),i.group(1),ico,'',mode,1,"else",True)
			additems(s)
	
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',makerequest(joinpath(datapath,'hdviet.html'))):
			addir(namecolor(name,c),href,icon['hdviet'],fanart,mode,page,'theloai',True)
	
	elif query=='3' and url==urlhome:#Phim l???
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',makerequest(joinpath(datapath,'hdviet.html')))
		for href,id,name in items:
			addir(namecolor(name,c),href,icon['hdviet'],fanart,mode,page,id,True)
	
	elif query=='10' and url==urlhome:#Phim b???
		body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim b??? ??u M??? %s'%name.strip()
			elif 'hong-kong' in href:name='Phim b??? H???ng K??ng %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim b??? Trung Qu???c %s'%name.strip()
			else:name='Phim b??? %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name,c),href,icon['hdviet'],fanart,mode,page,id,True)
	
	elif query=='hdvietfolder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response or int(response["Sequence"])==0:
			addir_info(namecolor(name),url,img,fanart,mode,page,'hdvietplay')
			return
		for eps in range(1,int(response["Sequence"])+1):
			name=re.sub(' \[COLOR green\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='T???p %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,'hdvietplay',False)
	
	elif query=='hdvietplay':
		link,sub=getResolvedUrl(url)#;print link,sub
		if not link:mess(u'Get link th???t b???i!','hdviet.com')
		else:
			if sub:
				mess(u'Ph??? ????? c???a HDViet.com','hdviet.com');xshare_resolve(sub)
				sub=urllib.unquote(os.path.splitext(os.path.basename(sub))[0])
			xbmcsetResolvedUrl(link,sub)
	
	elif query=='Themmucyeuthich':
		hd['Cookie']=getcookie()
		body=make_post('http://movies.hdviet.com/them-phim-yeu-thich.html',hd,urllib.urlencode({"MovieID":"%s"%url}))
		try:mess(body.json['r'],'hdviet.com')
		except:mess(u'L???i th??m phim y??u th??ch!','hdviet.com')
	
	else:
		if query=='yeu-thich':hd['Cookie']=getcookie();body=make_request(url,hd)
		else:body=make_request(url)
		body=sub_body(body,'class="homesection"','class="h2-ttl cf"')
		additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',sub_body(body,'class="active"',''))
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang ti???p theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,True)
		xbmc.executebuiltin('Container.SetViewMode(504)')

def hdviet1(name,url,img,mode,page,query):
	color['hdviet']='[COLOR darkorange]';icon['hdviet']=os.path.join(iconpath,'hdviet.png')
	homepage='http://movies.hdviet.com/'
	if os.path.isfile(joinpath(datapath,'hdviet.cookie')):os.remove(joinpath(datapath,'hdviet.cookie'))
	direct_link='https://api-v2.hdviet.com/movie/play?accesstokenkey=%s&movieid=%s'
	def namecolor(name):return '%s%s[/COLOR]'%(color['hdviet'],name)
	def getcookie():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		return response.cookiestring
	def login_hdviet():
		u=myaddon.getSetting('userhdviet');p=myaddon.getSetting('passhdviet')
		'''
		url='https://id.hdviet.com/authentication/login'
		response=make_post(url,data='email=%s&password=%s'%(u,p),resp='j')
		if response and response.get('error')==0:
			response=response.get('data')
			mess(u'Login th??nh c??ng','hdviet.com')
			json_rw('hdviet.cookie',response)
		elif response and response.get('error')==27:
			mess(u'Acc b??? kh??a t???m th???i. V??o web ????? login nh??!','hdviet.com');response=dict()
		elif response and response.get('error') in (25,22):
			mess(response.get('message'),'hdviet.com');response=dict()
		else:
		'''
		import hashlib;data=urllib.urlencode({'email':u,'password':hashlib.md5(p).hexdigest()})
		response=make_post('http://movies.hdviet.com/dang-nhap.html',hd,data)
		try:resp=response.json
		except:resp={u'r': u'L???i ????ng nh???p hdviet.com', u'e': 3}
		if resp.get('e')==0:
			mess(resp.get('r'),'hdviet.com');hd['Cookie']=response.cookiestring
			response=make_request('http://movies.hdviet.com/dieu-khoan-su-dung.html',headers=hd)
			import base64;token=base64.b64decode(xsearch('<a class="userinfo".+?token=(.+?)"',response))
			response={'Cookie':hd['Cookie'],'access_token':token};json_rw('hdviet.cookie',response)
		else:response=dict();mess(resp.get('r'),'hdviet.com')
		url='http://movies.hdviet.com/dang-xuat.html?accesstokenkey=%s'
		make_post(url%response.get('access_token')).body
		return response
	def getResolvedUrl(id_film,loop=0):#Phim le/phim chieu/ke doi dau thien ac
		def getlinkhdviet(token,id_film):
			id_film=id_film.replace('_e','&ep=')
			response=make_request(direct_link%(token,id_film),resp='j')
			try:links=response['r']
			except:links=dict()
			return links
		
		data=json_rw('hdviet.cookie')
		links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		if not link:return '',''
		elif '0000000000000000000000' in link:
			data=login_hdviet();links=getlinkhdviet(data.get('access_token'),id_film);link=links.get('LinkPlay')
		if link:
			max_resolution='_1920_' if myaddon.getSetting('hdvietresolution')=='1080' else '_1280_'
			resolutions=['_1920_','_1885_','_1876_','_1866_','_1792_','_1280_','_1024_','_800_','_640_','_480_']
			if '_e' in id_film:link=re.sub('%s_e\d{1,3}_'%id_film.split('_')[0],'%s_'%id_film,link)
			r=''.join([s for s in resolutions if s in link]);response=''
			if r:
				href=link[:link.rfind(r)]+link[link.rfind(r):].replace(r,'%s')
				for i in resolutions:
					if i>max_resolution:continue
					response=make_request(href%i)
					if len(response)>0:link=href%i;break
			else:response=make_request(link)
			if response:
				

				items=re.findall('RESOLUTION=(\d+?)x.*\s(.+m3u8)',response)
				if items:
					res=0;hr=''
					for r,h in items:
						if int(r)>res:res=int(r);hr=h
					if hr and 'http://' in hr:link=hr
					else:link=os.path.dirname(link)+'/'+hr
				else:
					items=re.findall('(.+m3u8)',response)
					if items and 'http://' in items[0]:link=items[len(items)-1]
					else:link=os.path.dirname(link)+'/'+items[0]

			else:link=''

		if not link:return '',''
		audio=links.get('AudioExt',list());audioindex=-1;linksub=''
		if len(audio)>1:
			audio_choice=myaddon.getSetting('hdvietaudio')
			if audio_choice=='H???i khi xem':
				title=u'[COLOR green]Ch???n Audio[/COLOR]';line1= u'[COLOR yellow]Vui l??ng ch???n Audio[/COLOR]'
				audioindex=mess_yesno(title,line1,'',audio[0].get("Label",'0'),audio[1].get("Label",'1'))
			else:audioindex=0 if u2s(audio[0].get("Label")) in audio_choice else 1
			if 'Thuy???t' not in u2s(audio[audioindex].get("Label")):linksub='yes'#b???t c??? download sub
			try:link=link+'?audioindex=%d'%(int(audio[audioindex].get("Index",'0'))-1)
			except:pass
		elif u2s(audio[0].get("Label"))=='Thuy???t Minh':audioindex=0
		if audioindex<0 or linksub:
			for source in ['Subtitle','SubtitleExt','SubtitleExtSe']:
				try:linksub=links[source]['VIE']['Source']
				except:linksub=''
				if linksub:break
		
		return link,linksub

	def additems(body):
		pattern='<li class="mov-item".+?href="(.+?)".+?src="(.+?)".+?title="Phim (.+?)".+?<span(.+?) data-id="(.+?)">'
		data=re.findall(pattern,body,re.DOTALL);listitems=list()
		for href,img,title,detail,id_film in data:
			epi=xsearch('"labelchap2">(\d{1,3})</span>',detail);title=unescape(title)
			res=xsearch('id="fillprofile" class="icon-(.+?)11">',detail)
			res='[COLOR gold]SD[/COLOR]' if 'SD' in res else '[COLOR gold]HD[/COLOR]%s'%res
			phim18=xsearch('class="children11".+?>(.+?)</label></span>',detail)
			TM=xsearch('id="fillaudio" class="icon-(.+?)">',detail)
			TM='%s[COLOR green]%s[/COLOR][COLOR red]%s[/COLOR]'%(res,TM,phim18)
			plot=xsearch('<span class="cot1">(.+?)</span>',detail)
			year=xsearch('<span class="chil-date".+?>(.*?)</label></span>',detail)
			act=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dien-vien/.+?">(.+?)</a>',detail))
			drt=', '.join(s for s in re.findall('<a href="http://movies.hdviet.com/dao-dien/.+?">(.+?)</a>',detail))
			rat=xsearch('<span class="fl-left">.+?<span>(.+?)</span>',detail)
			upl=xsearch('<span class="fl-right">.+?<span>(.+?)</span>',detail)
			if not epi:title=TM+' '+title;query='hdvietplay'
			elif epi=='1':query='hdvietfolder'
			else:title=TM+' '+namecolor(title)+' [COLOR green](%s)[/COLOR]'%epi;query='hdvietfolder'
			listItem = xbmcgui.ListItem(label=title,iconImage=img,thumbnailImage=img)
			if rat:rat='[COLOR tomato]IMDb:[/COLOR] %s, '%rat
			if upl:upl='[COLOR tomato]Uploader:[/COLOR] %s, '%upl
			if act:act='[COLOR tomato]Di???nvi??n:[/COLOR] %s, '%act
			if drt:drt='[COLOR tomato]?????odi???n:[/COLOR] %s, '%drt
			plot=rat+upl+act+drt+'\n'+plot
			info={'title':title,'year':year,'rating':xsearch('(\d\.\d{1,2})',rat),'plot':plot,'episode':epi,'director':drt,'writer':act}
			listItem.setInfo(type="Video", infoLabels=info)
			listItem.setArt({"thumb":img,"poster":img,"fanart":img})
			if query=='hdvietplay':listItem.setProperty('IsPlayable', 'true')
			u=sys.argv[0]+"?url="+id_film+"&img="+urllib.quote_plus(img)+"&fanart="+urllib.quote_plus(img)+"&mode="+str(mode)+"&page="+str(page)+"&query="+query+"&name="+urllib.quote_plus(title)
			listitems.append((u,listItem,False if query=='hdvietplay' else True))
		xbmcplugin.addDirectoryItems(int(sys.argv[1]),listitems,totalItems=len(listitems))
	def hdviet_search(string):
		url='http://movies.hdviet.com/tim-kiem.html?keyword=%s'%urllib.quote_plus(string)
		hdviet(name,url,img,mode,page,query='timkiem')
	if query=='hdviet.com':
		name=color['search']+"Search tr??n hdviet.com[/COLOR] (H??y ch???n ????? ph??n gi???i tr??n settings nh??)"
		addir(name,'http://movies.hdviet.com/tim-kiem.html',icon['icon'],fanart,mode,1,'search',True)
		href='http://movies.hdviet.com/phim-yeu-thich.html'
		addir(color['search']+'Phim y??u th??ch c???a t??i tr??n hdviet[/COLOR]',href,icon['icon'],fanart,mode,1,'yeu-thich',True)
		if checkupdate('hdviet.html',8):body=makerequest(joinpath(datapath,'hdviet.html'),make_request(homepage),'w')
		else:body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('"mainitem" menuid="(.+?)" href="(.+?)" title=".+?">(.+?)</a>',body)
		for id,href,name in items:
			addir(namecolor(name),homepage,icon['hdviet'],fanart,mode,1,id,True)
		addir(namecolor('Th??? lo???i phim'),'the-loai',icon['icon'],fanart,mode,1,'the-loai-phim',True)
		items=re.findall('<div class="h2-ttl cf">.+?<a href="(.+?)" title=".+?" >(.+?)</a>.+?</div>(.+?)</ul>',body,re.DOTALL)
		for href,name,subbody in items:
			addir('-----%s%s-----[/COLOR]'%(color['search'],name),href,icon['hdviet'],fanart,mode,page,'1',True)
			additems(subbody)
	elif query=='search':make_mySearch('','hdviet.com','','',mode,'get')
	elif query=="INP":hdviet_search(make_mySearch('',url,'','','','Input'))
	elif url=='hdviet.com':page=1 if 'Trang ti???p theo' not in name else page;hdviet_search(query)
	elif query=='the-loai-phim':
		for href,name in re.findall('<p><a href="(.+?)" title=".+?">(.+?)</a></p>',makerequest(joinpath(datapath,'hdviet.html'))):
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,'theloai',True)
	elif query=='3' and url==homepage:#Phim l???
		items=re.findall('<a href="(.+?)" .?menuid="(.+?)" .?title=".+?" >(.+?)</a>',makerequest(joinpath(datapath,'hdviet.html')))
		for href,id,name in items:
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='10' and url==homepage:#Phim b???
		body=makerequest(joinpath(datapath,'hdviet.html'))
		items=re.findall('<a href="(.+?)" menuid="(.+?)" title=".+?">(.+?)</a>',body)
		items+=re.findall('<a class="childparentlib" menuid="(.+?)" href="(.+?)" title=".+?">(\s.*.+?)</a>',body)
		for href,id,name in items:
			if 'au-my' in href:name='Phim b??? ??u M??? %s'%name.strip()
			elif 'hong-kong' in href:name='Phim b??? H???ng K??ng %s'%name.strip()
			elif 'trung-quoc' in href:name='Phim b??? Trung Qu???c %s'%name.strip()
			else:name='Phim b??? %s'%name.strip()
			if href in '38-39-40':temp=href;href=id;id=temp
			addir(namecolor(name),href,icon['hdviet'],fanart,mode,page,id,True)
	elif query=='hdvietfolder':
		href='http://movies.hdviet.com/lay-danh-sach-tap-phim.html?id=%s'%url
		response=make_request(href,resp='j')
		if not response:return
		for eps in range(1,int(response["Sequence"])+1):
			name=re.sub(' \[COLOR green\]\(\d{1,4}\)\[/COLOR\]','',name)
			title='T???p %s/%s-%s'%(format(eps,'0%dd'%len(response['Episode'])),str(response['Episode']),re.sub('\[.?COLOR.{,12}\]','',name))
			addir(title,'%s_e%d'%(url,eps),img,fanart,mode,page,'hdvietplay',False)
	elif query=='hdvietplay':
		link,sub=getResolvedUrl(url)#;print link,sub
		if not link:mess(u'Get link th???t b???i!','hdviet.com')
		else:
			if sub:
				mess(u'Ph??? ????? c???a HDViet.com','hdviet.com');xshare_resolve(sub)
				sub=urllib.unquote(os.path.splitext(os.path.basename(sub))[0])
			xbmcsetResolvedUrl(link,sub)
	elif query=='Themmucyeuthich':
		hd['Cookie']=getcookie()
		body=make_post('http://movies.hdviet.com/them-phim-yeu-thich.html',hd,urllib.urlencode({"MovieID":"%s"%url}))
		try:mess(body.json['r'],'hdviet.com')
		except:mess(u'L???i th??m phim y??u th??ch!','hdviet.com')
	else:
		if query=='yeu-thich':hd['Cookie']=getcookie();body=make_request(url,hd)
		else:body=make_request(url)
		body=sub_body(body,'class="homesection"','class="h2-ttl cf"')
		additems(body)
		pages=re.findall('<li class=""><a href="(.+?)">(.+?)</a></li>',sub_body(body,'class="active"',''))
		if pages:
			pagenext=pages[0][1];pageend=pages[len(pages)-1][1]
			name='%sTrang ti???p theo: trang %s/%s[/COLOR]'%(color['trangtiep'],pagenext,pageend)
			addir(name,pages[0][0],img,fanart,mode,page,query,True)
		xbmc.executebuiltin('Container.SetViewMode(504)')

def play_youtube(url):#https://www.youtube.com/get_video_info?video_id=xhNy0jnAgzI
	from resources.lib.servers import youtube;yt=youtube(url)
	items=yt.getData();link=''
	if items:
		for href,label in items:
			link=dl(href)
			if link:break
		if link:
			xbmcsetResolvedUrl(link,re.sub(' \[COLOR.+?/COLOR\]','',name)+'Maxlink')
			mess('Xshare playing on youtube.com')
		else:mess('Get maxspeed link fail!','youtube.com')
	else:mess('Video not found!','youtube.com')

def hayhaytv(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'hayhaytv.png');c='tomato';urlhome='http://www.hayhaytv.vn/'
	api='http://api.hayhaytv.vn/'
	hd={'User-Agent':'Mozilla/5.0 Gecko/20100101 Firefox/44.0'}
	hd['Cookie']=makerequest(joinpath(xsharefolder,'hayhaytv.cookie'))
	
	def detail(s):
		href=xsearch('href="(.+?)"',s)
		img=xsearch('src="(.+?)"',s)
		title=xsearch('alt="(.+?)"',s)
		if [i for i in (href,img,title) if not i]:return
		eps=re.sub('<strong>','',xsearch('<span class="label-range">(.+?)</strong>',s).strip())
		if not eps:addir_info(title,href,img,'',mode,1,'play')
		else:addir_info(namecolor(title,c)+' [COLOR blue]%s[/COLOR]'%eps,href,img,'',mode,page,'eps',True)
	
	if query=='hayhaytv.vn':
		body=re.sub('>\s*<','><',get_home_page('hayhaytv.html',urlhome))
		title=color['search']+"Search tr??n hayhaytv.vn (director/film/actor/show)[/COLOR]"
		addir_info(title,'hayhaytv.vn',ico,'',mode,1,'search',True)
		
		for href,title in [("phim-le.html",'PHIM L???'),("phim-bo.html","PHIM B???"),("show.html","SHOW"),("","TH??? LO???I"),("","QU???C GIA"),("","N??M PH??T H??NH")]:
			if href:href='http://www.hayhaytv.vn/'+href;query='page'
			else:query='menu'
			addir_info(namecolor(title,c),href,ico,'',mode,1,query,True)
		
		S=body.split('<div class="group-title-bg">')
		t=''.join(i for i in S if '>XEM NHI???U</a>' in i)
		s=[i for i in t.split('id="content_') if '<h3>' in i]
		
		for s in s:
			add_sep_item('-----------%s-----------'%xsearch('<h3>(.+?)</h3>',s))
			for s in re.findall('(<li.+?/li>)',s):detail(s)
			
		for s in S:
			label=re.search('<span class="title\d+"><a href="([^"]+)">([^<]+)</a>',s)
			if label:
				title='[COLOR lime]-----------%s-----------[/COLOR]'%label.group(2)
				href=label.group(1)
				if 'http' not in href:href='http://www.hayhaytv.vn'+href
				addir_info(title,href,ico,'',mode,page,'page',True)
				
				s=xsearch('(<ul.+?/ul>)',s,1,re.DOTALL)
				t=('<div class="block-base movie">','<div class="block-base movie clearfix">','<div class="block-base movie clearfix">','class="ntipse"')
				for i in t:
					if i in s:s=s.split(i);t='';break
				if t:return	
				
				for s in s:detail(s)
					
			elif '<div id="main-banner">' in s:
				add_sep_item('-----------Hayhaytv gi???i thi???u-----------')
				for href,t1,t2 in re.findall('<a href="([^"]+)"><[^<]+>([^<]+)<.+?>([^<]+)</span>',s):
					title=t1+' - '+t2
					img=xsearch('<a href="%s"><img[^<]+src="([^"]+)"'%href,s)
					addir_info(namecolor(title,c),href,img,img,mode,1,'eps',True)

		if get_home_page('hayhaytv.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="hayhaytv.vn":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query.strip():return
		search_string = urllib.quote_plus(query)
		url='http://www.hayhaytv.vn/tim-kiem.html?term='+search_string
		hd={'User-Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}
		try:j=json.loads(xread(url,{'User-Agent':'Mozilla/5.0','X-Requested-With':'XMLHttpRequest'}))
		except:j={}
		for s in ('director','phim','actor','show'):
			for i in j.get(s,[]):
				title=i.get('name').encode('utf-8')+' - '+i.get('extension').encode('utf-8')
				href=i.get('link')
				img=i.get('image')
				eps=(i.get('last_episode')+'/'+i.get('total_episode')) if i.get('total_episode')>'1' else ''
				eps=eps.encode('utf-8')
				if not eps:addir_info(title,href,img,'',mode,1,'play')
				else:addir_info(namecolor(title,c)+' [COLOR blue]%s[/COLOR]'%eps,href,img,'',mode,page,'eps',True)

	elif query=="menu":
		b=re.sub('>\s*<','><',get_home_page('hayhaytv.html',urlhome))
		S=' '.join(i for i in b.split('class="tnico-') if namecolor(name) in i)
		for href,title in re.findall('href="([^"]+?)".*?>([^"]+?)</a>',S):
			if 'http' not in href:href='http://www.hayhaytv.vn'+href
			addir_info(namecolor(title,c),href,ico,'',mode,page,'page',True)
		
	elif query=="page":
		b=re.sub('>\s*<','><',xread(url))
		p1='<div class="group-title">';p2='<div class="block-base movie">'
		S=' '.join(i for i in b.split(p1) if p2 in i)
		for s in S.split(p2):detail(s)
		
		pn=xsearch('<a href="([^"]+?)">Sau</a>',S)
		if pn:
			pages=xsearch('<a href="[^"]+page=(\d+)">Cu???i</a>',S)
			name=re.sub('\[COLOR %s.+/COLOR\]'%color['trangtiep'],'',name)
			title=name+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page+1,pages)
			if 'http' not in pn:pn='http://www.hayhaytv.vn'+pn
			addir_info(title,pn,ico,'',mode,page+1,query,True)

	elif query=="eps":
		b=re.sub('>\s*<','><',xread(url))
		s=re.findall('<a class="ep-link.+?href="(.+?)">(.+?)</a>',b)
		if not s:
			addir_info(namecolor(name),url,img,'',mode,1,'play')
		else:
			for href,title in s:
				addir_info('T???p '+title+' '+namecolor(name),href,img,'',mode,1,'play')
	
	elif query=="play":
		from resources.lib.servers import hayhayvn;hh=hayhayvn(c)
		link,sub=hh.getLink(url)
		if link:
			if sub:
				s=xread(sub)
				sub=joinpath(subsfolder,'hayhay-Vie.sub')
				makerequest(sub,s,'wb')
			xbmcsetResolvedUrl(link,sub)
		else:mess('File invalid or deleted!','hayhaytv.vn') 
		
	elif query=="play":
		b=xread(url)
		url='http://www.hayhaytv.vn/getsource/%s'%xsearch("FILM_KEY = '(.+?)'",b)
		b=xread(url,{'Referer':'http://www.hayhaytv.vn/'})
		try:j=eval(b)
		except:j=[]
		s=[(i.get('file').replace('\\',''),i.get('label')) for i in j]
		link=''
		if s:
			L=sorted(s, key=lambda k: k[1],reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print href,L
			for href,r in L:
				link=dl(href)#;print 'a',link,'b',href
				if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','hayhaytv.vn') 
			
	elif query=="play":
		b=xread(url)
		s=re.findall("file:'([^']+?)',label:'([^']+?)'",b)
		link=''
		if s:
			L=list(set([(i[0],resolu(i[1])) for i in s]))#;print L
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print href,L
			for href,r in L:
				link=dl(href)#;print 'a',link,'b',href
				if link:break
		else:
			s=list(set(re.findall("file:.?'([^']+)'",b)))#;print s
			for href in s:
				if 'm3u8' in href:link=href;break
			if not link:
				for href in s:
					if 'youtube.com' in href:link=href;break
		if 'youtube.com' in link:play_youtube(link)
		elif link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phimbathu.com') 

def phimmoi(name,url,img,mode,page,query):
	color['phimmoi']='[COLOR ghostwhite]';icon['phimmoi']=os.path.join(iconpath,'phimmoi.png')
	urlhome='http://www.phimmoi.net/';refresh=False;phimmoixml=joinpath(datapath,'phimmoi.xml')
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimmoi'],name)
	def login_pm():
		u=myaddon.getSetting('userphimmoi');p=myaddon.getSetting('passphimmoi')
		p=urllib2.hashlib.md5(p).hexdigest()
		response=make_post('http://www.phimmoi.net/login/',data=urllib.urlencode({'username':u,'password_md5':p}))
		if response.status==302 and makerequest(joinpath(datapath,'phimmoi.cookie'),response.cookiestring,'w'):
			mess(u'Login th??nh c??ng','phimmoi.net');f=response.cookiestring
		else:mess(u'Login kh??ng th??nh c??ng!','phimmoi.net');f=''
		return f
	
	def get_token(hd={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'},token=''):
		if not checkupdate('phimmoi.cookie',hours=24):
			hd['Cookie']=makerequest(joinpath(datapath,'phimmoi.cookie'));url='http://www.phimmoi.net/tu-phim/'
			body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body)
		if not token:
			hd['Cookie']=login_pm();body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body)
		return body,token,hd
	
	def getoken():
		_0xc3c8x48=str(int(round(time.time())))
		_0xc3c8x49=urllib2.hashlib.md5(_0xc3c8x48+'(*Y#NFJKDHFIEY#(**%#&*^%').hexdigest()
		return _0xc3c8x49[:11]+_0xc3c8x48+_0xc3c8x49[21:32]
	
	def pm_search(string):
		url='http://www.phimmoi.net/tim-kiem/%s/'%urllib.quote_plus(string)
		phimmoi(name,url,img,mode,page=1,query='readpage')
	
	def get_language(language):
		if language=='subtitle':language='Vietsub'
		elif language=='illustrate':language='Thuy???t minh'
		elif language=='dubbing':language='L???ng ti???ng'
		else:language=''
		return language
	
	def get_epi(epi):
		try:epi=int(epi)
		except:epi=0
		return epi
	
	def pm_get_info(title,href,img,detail):
		eps=xsearch('T???p ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail)
		if not eps:
			epi=xsearch('class="eps">Tr???n b??? ?(\d{1,4}) ?t???p</div>',detail)
			if epi:eps='%s/%s'%(epi,epi)
		else:epi=eps.split('/')[0]
		dur=xsearch('>(\d{1,3}.?ph??t)',detail)
		audio='TM' if 'Thuy???t minh' in detail else ''
		label=xsearch('(HD[\w|-]*|SD[\w|-]*|B???n ?????p[\w|-]*)',detail)
		if 'url=' in img:img=img.split('url=')[1]
		if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
		if 'ph??t/t???p' in detail:
			title='%s [COLOR gold]%s[/COLOR]'%(title,xsearch('>(\d{1,3} ph??t/t???p)<',detail))
		elif dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
		if xsearch('<span class="ribbon">Trailer</span>',detail,0):query='pmplay_trailer'
		elif get_epi(epi)>1 or 'ph??t/t???p' in detail or 'Phim b??? hot trong tu???n' in name:
			query='pmfolder';title=namecolor(title)
		else:query='pm_list_url_ple'
		if audio:title='[COLOR gold]TM[/COLOR] %s'%title
		if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
		return title,urlhome+href,img,query
	
	def pmaddir(items,action='Add'):#title,href,img,detail
		for title,href,img,detail in items:
			title,href,img,query=pm_get_info(title,href,img,detail)
			menu={'tuphim':{'action':action,'server':['phimmoi.net']}}
			addir_info(title,href,img,'',mode,page,query,True if query!='pmplay_trailer' else False,menu=menu)
	
	def pm_get_maxlink(google_link):
		href=urlhome+'player/v1.46/plugins/gkplugins_picasa2gdocs/plugins/plugins_player.php?url=%s&token=%s'
		result=make_post(href%(google_link,getoken()),resp='j')
		height=0;link='';maxresolution=int(myaddon.getSetting('phimmoiresolution'))
		for item in [s for s in result.get("content",list()) if 'video' in s.get('type')]:
			if item.get('height',0)==maxresolution:link=item.get('url');break
			elif item.get('height',0)>height:height=item.get('height',0);link=item.get('url')
		return link

	if query=='phimmoi.net':
		name=color['search']+"Search tr??n phimmoi.net[/COLOR] (Ch???n ????? ph??n gi???i max tr??n settings nh??)"
		addir_info(name,'http://www.phimmoi.net/tim-kiem/',icon['phimmoi'],'',mode,1,'search',True)
		name=color['search']+'T??? phim tr??n phimmoi.net c???a t??i[/COLOR]'
		addir_info(name,'http://www.phimmoi.net/tu-phim/',img,'',mode,1,'readpage',True)
		body=get_home_page('phimmoi.html',urlhome)
		content=xsearch('<ul id=".+?"(.+?)</ul></div>',body)
		for title in re.findall('<a>(.+?)</a>',content):
			addir_info(namecolor(title),'',icon['phimmoi'],'',mode,1,'menubar',True)
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			addir_info(namecolor(title),href,icon['phimmoi'],'',mode,1,'menubar',True)
		for title in re.findall('<h2 class="right-box-header star-icon"><span>(.+?)</span>',body):
			if title=='Phim ???? ????nh d???u':continue
			addir_info(namecolor(title),'right-box',img,'',mode,1,'menubar',True)
		for label,content in re.findall('class="title-list-index">(.+?)</span>(.+?</div></div></div>)',body):
			add_sep_item(label)
			#addir_info('[COLOR lime]%s[/COLOR]'%label,'',img,'',mode,1,'no')
			pattern='<li><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)".+?(<h3.+?</p>)'
			items=re.findall(pattern,content)
			if items:pmaddir([(s[1],s[0],s[2],s[3]) for s in items])#title,href,img,detail
			else:
				pattern='"movie-item m-block" title="(.+?)" href="(.+?)".+?(http.+?\.jpg).+?<div(.+?)</div></a></li>'
				pmaddir(re.findall(pattern,content))#title,href,img,detail
			if label=='Phim ????? c???':
				for title,content in re.findall('<h2 class="hidden">(.+?)</h2>(.+?</li></ul>)',body):
					add_sep_item(title)
					#addir_info('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
					pattern='title="(.+?)" href="(.+?)".+?\(\'(http.+?)\'\).+?</div></a>(.+?)</div></li>'
					pmaddir(re.findall(pattern,content))#title,href,img,detail
		if get_home_page('phimmoi.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=='search':make_mySearch('','phimmoi.net','','',mode,'get')
	elif query=="INP":pm_search(make_mySearch('',url,'','','','Input'))
	elif url=='phimmoi.net':page=1 if 'Trang ti???p theo' not in name else page;pm_search(query)
	
	elif query=='menubar':
		if any(s for s in ['kinh','rap','tags','trailer'] if s in url):
			if 'tags' not in url:url=urlhome+url
			return phimmoi(name,url,img,mode,page,'readpage')
		elif url=='right-box':
			pattern='<span>%s</span>(.+?</li></ul></div></div>)'%re.sub('\[/?COLOR.*?\]','',name).strip()
			content=xsearch(pattern,makerequest(joinpath(xsharefolder,'phimmoi.html')))
			pattern='title="(.+?)" href="(.+?)">.+?\(\'(.+?)\'\).+?</span>(.+?)</a></li>'
			pmaddir(re.findall(pattern,content))#title,href,img,detail
		else:
			content=xsearch('<ul id=".+?"(.+?)</ul></div>',makerequest(joinpath(xsharefolder,'phimmoi.html')))
			gen={'Th??? lo???i':'the-loai','Qu???c gia':'quoc-gia','Phim l???':'phim-le','Phim b???':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',name).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content):
				addir_info(namecolor(title),urlhome+href,icon['phimmoi'],'',mode,1,'readpage',True)
	
	elif query=='readpage':
		if url=='http://www.phimmoi.net/tu-phim/':body,token,headers=get_token();action='Remove'
		else:body=make_request(url);action='Add'
		menu={'tuphim':{'action':action,'server':['phimmoi.net']}}
		for s in re.findall('(<li class="movie-item">.+?</li>)',body,re.DOTALL):
			title=xsearch('title="(.+?)"',s)
			#label=xsearch('"ribbon">(.+?)</span>',s)
			#if label:title+=' [COLOR green]%s[/COLOR]'%label
			href=xsearch('href="(.+?)"',s)
			#if '//' not in href:href=urlhome+href
			img=xsearch('url=(.+?)%',s)
			title,href,img,query=pm_get_info(title,href,img,s)
			addir_info(title,href,img,'',mode,page,query,True,menu=menu)
			
		urlnext=xsearch('<li><a href="(.+?)">Trang k???.+?</a></li>',body)
		if urlnext:
			pagenext=xsearch('/page-(\d{1,3})\.html',urlnext)
			name='%sTrang ti???p theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			addir_info(name,urlhome+urlnext,img,fanart,mode,page,'readpage',True)

	elif query=='readpage1':
		if url=='http://www.phimmoi.net/tu-phim/':body,token,headers=get_token();menu='Remove'
		else:body=make_request(url);menu='Add'
		pattern='<li class="movie-item">.+?title="(.+?)" href="(.+?)".+?(http.+?)\)(.+?)</li>'
		pmaddir(re.findall(pattern,body,re.DOTALL),menu)#title,href,img,detail
		urlnext=xsearch('<li><a href="(.+?)">Trang k???.+?</a></li>',body)
		if urlnext:
			pagenext=xsearch('/page-(\d{1,3})\.html',urlnext)
			name='%sTrang ti???p theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			addir_info(name,urlhome+urlnext,img,fanart,mode,page,'readpage',True)
	
	elif 'tuphim' in query:
		body,token,headers=get_token();data={'_fxAjax':'1','_fxResponseType':'JSON','_fxToken':'%s'%token}
		action='add' if 'Add' in query else 'remove'
		response=make_post('%s%s.html'%(url,action),headers,data,resp='j')
		if response.get('_fxStatus',0)==1:
			mess(response.get('_fxMessage','success'),'phimmoi.net')
			if action=='remove':xbmc.executebuiltin("Container.Refresh")
		else:
			try:mess(response.get('_fxErrors')[0],'phimmoi.net')
			except:mess(u'???? ph??t sinh l???i!','phimmoi.net')
	
	elif query=='pmfolder':
		body=make_request(url+'xem-phim.html')
		menu={'tuphim':{'action':'Add','server':['phimmoi.net']}}
		eps=xsearch('(/\d{1,4})\)',name)
		name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} ph??t/t???p|\d{1,3} ph??t','',name).strip()
		
		for detail in re.findall('(<div class="server clearfix server-group".+?</ul>)',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 't???p phim' not in title:
				serverid=xsearch('data-serverid="(.+?)"',detail)
				add_sep_item('-------%s-------'%(title+' - '+serverid))
			label=name.replace('TM ','') if title and 'Thuy???t minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				addir_info('%s%s %s'%(title,eps,label),urlhome+href,img,'',mode,page,'pm_play',menu=menu)
	
	elif query=='pm_list_url_ple':
		body=make_request(url if '.html' in url else url+'xem-phim.html')
		
		#Doan nay moi bo sung, chua fix doan duoi-----------------------------------------
		u=xsearch('src="([^<]*?episodeinfo.+?)"',body)
		if 'http://' not in u:u='http://www.phimmoi.net/'+u
		hd['Referer']=url
		b=make_request(u,hd)
		c=xsearch("_responseJson='(.+?)'",b)
		try:d=json.loads(c.replace('\\',''))
		except:d={}
		
		href='';height=width=0
		for i in d.get('medias',[]):
			if i.get('height',0)>height:height=i.get('height');href=i.get('url')
			if i.get('width',0)>width:width=i.get('width');href=i.get('url')
		if href:
			s=make_request(href,resp='o')
			if s and s.status==302:
				href=s.headers.get('location')
				addir_info(name,href,img,'',mode,page,'pmplay_ple_')
		#----------------------------------------------------------------------------------
		
		content=xsearch('<div class="list-server">(.+?)</div>',body,1,re.DOTALL).replace('\n','')
		for label,subcontent in re.findall('class="server-title">(.+?)</h3>(.+?)</ul>',content):
			for href,title in re.findall('href="(.+?)">(.+?)</a>',subcontent):
				addir_info('%s %s'%(label,title),urlhome+href,img,'',mode,page,'pm_play')
			
		episodeJson=xsearch("episodeJson='(.+?)'",body)
		try:episodeJson=eval(episodeJson)
		except:return
		for i in [s for s in episodeJson if s.get('url')]:
			language=get_language(i.get('language'));part=i.get('part',0)
			if part<parts:server+=1;parts=0
			else:parts=part
			numserver='S%d'%server if server%2==0 else '[COLOR green]S%d[/COLOR]'%server
			if part==0:label='[COLOR gold]%s %s[/COLOR]: '%(numserver,language)+name;server+=1
			else:
				label='[COLOR gold]%s-part%d-%s[/COLOR]: '%(numserver,part,language)
				label+=re.sub('\[COLOR gold\].{1,5}ph??t\[/COLOR\] - ','',name)
			addir_info(label,i['url'].replace('\\',''),img,art,mode,page,'pmplay_ple')
	
	elif query=='pm_play':
		url=url if '.html' in url else url+'xem-phim.html'
		body=make_request(url)
		u=xsearch('src="([^<]*?episodeinfo.+?)"',body)
		if 'http://' not in u:u='http://www.phimmoi.net/'+u
		hd['Referer']=url
		b=make_request(u,hd)
		c=xsearch("_responseJson='(.+?)'",b);href=''
		try:d=json.loads(c.replace('\\',''))
		except:d={}
		#print u,c,d
		L=[]
		if d.get('medias'):
			try:L=[(s.get('url'),resolu(str(s.get('resolution')))) for s in d.get('medias')]
			except:L=[]
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
		elif d.get('url'):L=[(d.get('url'),'1')]
		
		link=''
		for href,label in L:
			link=dl(href)
			if link:break
		
		if link:xbmcsetResolvedUrl(link)
		else:mess(u'Kh??ng get ???????c maxspeedlink ho???c link b??? die!','phimmoi.net')

	elif query=='pmplay_ple_':xbmcsetResolvedUrl(url)
	elif query=='pmplay_ple':
		href=pm_get_maxlink(url)
		if href:xbmcsetResolvedUrl(href)
		else:mess(u'Kh??ng get ???????c maxspeedlink ho???c link b??? die!','phimmoi.net')
	
	elif query=='pmplay_pbo':
		
		#Doan nay moi bo sung, chua fix doan duoi-----------------------------------------
		b=make_request('http://www.phimmoi.net/'+xsearch('src="(episodeinfo.+?)"',make_request(url)))
		c=xsearch("_responseJson='(.+?)'",b);d=json.loads(c)
				
		href='';height=width=0	
		for i in d.get('medias'):
			if i.get('height')>height:height=i.get('height');href=i.get('url').replace('\\','')
			if i.get('width')>width:width=i.get('width');href=i.get('url').replace('\\','')
		if href:
			s=make_request(href,resp='o')
			if s and s.status==302:
				href=s.headers.get('location')
				xbmcsetResolvedUrl(href)
			elif d.get('notice'):
				try:mess(d.get('notice')[0].replace(',',''),'phimmoi.net')
				except:mess(u'Kh??ng get ???????c maxspeedlink ho???c link b??? die!','phimmoi.net')
		else:mess(u'Kh??ng get ???????c maxspeedlink ho???c link b??? die!','phimmoi.net')
		#----------------------------------------------------------------------------------
		
	elif query=='pmplay_pbo_':
		href=pm_get_maxlink(xsearch("currentEpisode.url='(.+?)'",make_request(url)))
		if href:xbmcsetResolvedUrl(href)
		else:mess(u'Kh??ng get ???????c maxspeedlink ho???c link b??? die!','phimmoi.net')
	
	elif query=='pmplay_trailer':
		href=xsearch("filmInfo.trailerUrl='(.+?)'",make_request(url))
		return play_youtube(href)

def phimmoi1(name,url,img,mode,page,query):
	color['phimmoi']='[COLOR ghostwhite]';icon['phimmoi']=os.path.join(iconpath,'phimmoi.png')
	urlhome='http://www.phimmoi.net/';refresh=False;phimmoixml=joinpath(datapath,'phimmoi.xml')
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimmoi'],name)
	def login_pm():
		u=myaddon.getSetting('userphimmoi');p=myaddon.getSetting('passphimmoi')
		import hashlib;p=hashlib.md5(p).hexdigest()
		response=make_post('http://www.phimmoi.net/login/',data=urllib.urlencode({'username':u,'password_md5':p}))
		if response.status==302 and makerequest(joinpath(datapath,'phimmoi.cookie'),response.cookiestring,'w'):
			mess(u'Login th??nh c??ng','phimmoi.net');f=response.cookiestring
		else:mess(u'Login kh??ng th??nh c??ng!','phimmoi.net');f=''
		return f
	def get_token(hd={'User-Agent':'Mozilla/5.0 Chrome/39.0.2171.71 Firefox/33.0'}):
		hd['Cookie']=makerequest(joinpath(datapath,'phimmoi.cookie'));url='http://www.phimmoi.net/tu-phim/'
		body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body)
		if not token:
			hd['Cookie']=login_pm();body=make_request(url,headers=hd);token=xsearch("fx\.token='(.+?)'",body)
		return body,token,hd
	def getoken():
		import time;_0xc3c8x48=str(int(round(time.time())))
		import hashlib;_0xc3c8x49=hashlib.md5(_0xc3c8x48+'(*Y#NFJKDHFIEY#(**%#&*^%').hexdigest()
		return _0xc3c8x49[:11]+_0xc3c8x48+_0xc3c8x49[21:32]
	def pm_search(string):
		url='http://www.phimmoi.net/tim-kiem/%s/'%urllib.quote_plus(string)
		phimmoi(name,url,img,mode,page=1,query='readpage')
	def get_language(language):
		if language=='subtitle':language='Vietsub'
		elif language=='illustrate':language='Thuy???t minh'
		elif language=='dubbing':language='L???ng ti???ng'
		else:language=''
		return language
	def get_epi(epi):
		try:epi=int(epi)
		except:epi=0
		return epi
	def pm_get_info(title,href,img,detail):
		eps=xsearch('T???p ?(\d{,4}/\d{,4}|\?/\d{,4}|\d{,4})',detail)
		if not eps:
			epi=xsearch('class="eps">Tr???n b??? ?(\d{1,4}) ?t???p</div>',detail)
			if epi:eps='%s/%s'%(epi,epi)
		else:epi=eps.split('/')[0]
		dur=xsearch('>(\d{1,3}.?ph??t)',detail)
		audio='TM' if 'Thuy???t minh' in detail else ''
		label=xsearch('(HD[\w|-]*|SD[\w|-]*|B???n ?????p[\w|-]*)',detail)
		if 'url=' in img:img=img.split('url=')[1]
		if eps:title='%s %s(%s)[/COLOR]'%(title,color['subscene'],eps)
		if 'ph??t/t???p' in detail:
			title='%s [COLOR gold]%s[/COLOR]'%(title,xsearch('>(\d{1,3} ph??t/t???p)<',detail))
		elif dur:title='%s [COLOR gold]%s[/COLOR]'%(title,dur)
		if xsearch('<span class="ribbon">Trailer</span>',detail,0):query='pmplay_trailer'
		elif get_epi(epi)>1 or 'ph??t/t???p' in detail or 'Phim b??? hot trong tu???n' in name:
			query='pmfolder';title=namecolor(title)
		else:query='pm_list_url_ple'
		if audio:title='[COLOR gold]TM[/COLOR] %s'%title
		if label:title='%s - [COLOR green]%s[/COLOR]'%(title,label)
		return title,urlhome+href,img,query
	def pmaddir(items,action='Add'):#title,href,img,detail
		for title,href,img,detail in items:
			title,href,img,query=pm_get_info(title,href,img,detail)
			menu={'tuphim':{'action':action,'server':['phimmoi.net']}}
			addir_info(title,href,img,'',mode,page,query,True if query!='pmplay_trailer' else False,menu=menu)
	def pm_get_maxlink(google_link):
		href=urlhome+'player/v1.46/plugins/gkplugins_picasa2gdocs/plugins/plugins_player.php?url=%s&token=%s'
		#print href%(google_link,getoken())
		result=make_post(href%(google_link,getoken()),resp='j')
		height=0;link='';maxresolution=int(myaddon.getSetting('phimmoiresolution'))
		for item in [s for s in result.get("content",list()) if 'video' in s.get('type')]:
			if item.get('height',0)==maxresolution:link=item.get('url');break
			elif item.get('height',0)>height:height=item.get('height',0);link=item.get('url')
		return link

	if query=='phimmoi.net':
		name=color['search']+"Search tr??n phimmoi.net[/COLOR] (Ch???n ????? ph??n gi???i max tr??n settings nh??)"
		addir_info(name,'http://www.phimmoi.net/tim-kiem/',icon['phimmoi'],'',mode,1,'search',True)
		name=color['search']+'T??? phim tr??n phimmoi.net c???a t??i[/COLOR]'
		addir_info(name,'http://www.phimmoi.net/tu-phim/',img,'',mode,1,'readpage',True)
		body=get_home_page('phimmoi.html',urlhome)
		content=xsearch('<ul id=".+?"(.+?)</ul></div>',body)
		for title in re.findall('<a>(.+?)</a>',content):
			addir_info(namecolor(title),'',icon['phimmoi'],'',mode,1,'menubar',True)
		for href,title in re.findall('<a href="([\w|-]+/|http://www.phimmoi.net/tags/.*?)">(.+?)</a>',content):
			addir_info(namecolor(title),href,icon['phimmoi'],'',mode,1,'menubar',True)
		for title in re.findall('<h2 class="right-box-header star-icon"><span>(.+?)</span>',body):
			if title=='Phim ???? ????nh d???u':continue
			addir_info(namecolor(title),'right-box',img,'',mode,1,'menubar',True)
		for label,content in re.findall('class="title-list-index">(.+?)</span>(.+?</div></div></div>)',body):
			add_sep_item(label)
			#addir_info('[COLOR lime]%s[/COLOR]'%label,'',img,'',mode,1,'no')
			pattern='<li><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)".+?(<h3.+?</p>)'
			items=re.findall(pattern,content)
			if items:pmaddir([(s[1],s[0],s[2],s[3]) for s in items])#title,href,img,detail
			else:
				pattern='"movie-item m-block" title="(.+?)" href="(.+?)".+?(http.+?\.jpg).+?<div(.+?)</div></a></li>'
				pmaddir(re.findall(pattern,content))#title,href,img,detail
			if label=='Phim ????? c???':
				for title,content in re.findall('<h2 class="hidden">(.+?)</h2>(.+?</li></ul>)',body):
					add_sep_item(title)
					#addir_info('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
					pattern='title="(.+?)" href="(.+?)".+?\(\'(http.+?)\'\).+?</div></a>(.+?)</div></li>'
					pmaddir(re.findall(pattern,content))#title,href,img,detail
		if get_home_page('phimmoi.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	elif query=='search':make_mySearch('','phimmoi.net','','',mode,'get')
	elif query=="INP":pm_search(make_mySearch('',url,'','','','Input'))
	elif url=='phimmoi.net':page=1 if 'Trang ti???p theo' not in name else page;pm_search(query)
	elif query=='menubar':
		if any(s for s in ['kinh','rap','tags','trailer'] if s in url):
			if 'tags' not in url:url=urlhome+url
			return phimmoi(name,url,img,mode,page,'readpage')
		elif url=='right-box':
			pattern='<span>%s</span>(.+?</li></ul></div></div>)'%re.sub('\[/?COLOR.*?\]','',name).strip()
			content=xsearch(pattern,makerequest(joinpath(xsharefolder,'phimmoi.html')))
			pattern='title="(.+?)" href="(.+?)">.+?\(\'(.+?)\'\).+?</span>(.+?)</a></li>'
			pmaddir(re.findall(pattern,content))#title,href,img,detail
		else:
			content=xsearch('<ul id=".+?"(.+?)</ul></div>',makerequest(joinpath(xsharefolder,'phimmoi.html')))
			gen={'Th??? lo???i':'the-loai','Qu???c gia':'quoc-gia','Phim l???':'phim-le','Phim b???':'phim-bo'}
			query=gen.get(re.sub('\[/?COLOR.*?\]|\(.+?\)','',name).strip())
			pattern='<a href="(%s/.*?)">(.+?)</a>'%query
			for href,title in re.findall(pattern,content):
				addir_info(namecolor(title),urlhome+href,icon['phimmoi'],'',mode,1,'readpage',True)
	elif query=='readpage':
		if url=='http://www.phimmoi.net/tu-phim/':body,token,headers=get_token();menu='Remove'
		else:body=make_request(url);menu='Add'
		pattern='<li class="movie-item">.+?title="(.+?)" href="(.+?)".+?(http.+?)\)(.+?)</li>'
		pmaddir(re.findall(pattern,body,re.DOTALL),menu)#title,href,img,detail
		urlnext=xsearch('<li><a href="(.+?)">Trang k???.+?</a></li>',body)
		if urlnext:
			pagenext=xsearch('/page-(\d{1,3})\.html',urlnext)
			name='%sTrang ti???p theo: trang %s[/COLOR]'%(color['trangtiep'],pagenext)
			addir_info(name,urlhome+urlnext,img,fanart,mode,page,'readpage',True)
	elif 'tuphim' in query:
		body,token,headers=get_token();data={'_fxAjax':'1','_fxResponseType':'JSON','_fxToken':'%s'%token}
		action='add' if 'Add' in query else 'remove'
		response=make_post('%s%s.html'%(url,action),headers,data,resp='j')
		if response.get('_fxStatus',0)==1:
			mess(response.get('_fxMessage','success'),'phimmoi.net')
			if action=='remove':xbmc.executebuiltin("Container.Refresh")
		else:
			try:mess(response.get('_fxErrors')[0],'phimmoi.net')
			except:mess(u'???? ph??t sinh l???i!','phimmoi.net')
	elif query=='pmfolder':
		body=make_request(url+'xem-phim.html');menu={'tuphim':{'action':'Add','server':['phimmoi.net']}}
		eps=xsearch('(/\d{1,4})\)',name);name=re.sub('\[/?COLOR.*?\]|\(.+?\)|\d{1,3} ph??t/t???p|\d{1,3} ph??t','',name).strip()
		for detail in re.findall('data-serverid="pcs"(.+?)</li></ul></div>',body,re.DOTALL):
			title=' '.join(s for s in xsearch('<h3 class="server-name">(.+?)</h3>',detail,1,re.DOTALL).split())
			if title and 't???p phim' not in title:
				add_sep_item(title)
				#addir_info('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			label=name.replace('TM ','') if title and 'Thuy???t minh' not in title else name
			for title,href in re.findall('title="(.+?)".+?href="(.+?)"',detail,re.DOTALL):
				addir_info('%s%s %s'%(title,eps,label),urlhome+href,img,'',mode,page,'pmplay_pbo',menu=menu)
	elif query=='pm_list_url_ple':
		body=make_request(url if '.html' in url else url+'xem-phim.html')
		if xsearch("filmInfo.isSeries=\('serial'=='serial'\)",body,0):return phimmoi(name,url,img,mode,page,'pmfolder')
		if xsearch("filmInfo.isAdult=parseInt\('1'\)",body,0) and myaddon.getSetting('phim18')=="false":
			return mess_yesno(line1='Phim n??y c?? c???nh quay nh???y c???m v?? b???n ???? ch???n kh??ng xem!', line2='Thanks you')
		art=xsearch("filmInfo.previewUrl='.+=(https:.+)'",body);name=name.replace('[COLOR gold]TM[/COLOR]','')
		link=xsearch("currentEpisode.url='(.+?)'",body);server=1;parts=0
		language=xsearch("currentEpisode.language='(.+?)'",body)
		label='[COLOR gold]S0 %s[/COLOR]: '%get_language(language)+name
		if link:addir_info(label,link,img,art,mode,page,'pmplay_ple')
		
		content=xsearch('<div class="list-server">(.+?)</div>',body,1,re.DOTALL).replace('\n','')
		for label,subcontent in re.findall('class="server-title">(.+?)</h3>(.+?)</ul>',content):
			for href,title in re.findall('href="(.+?)">(.+?)</a>',subcontent):
				addir_info('%s %s'%(label,title),urlhome+href,img,art,mode,page,'pmplay_pbo')
			
		episodeJson=xsearch("episodeJson='(.+?)'",body)
		try:episodeJson=eval(episodeJson)
		except:return
		for i in [s for s in episodeJson if s.get('url')]:
			language=get_language(i.get('language'));part=i.get('part',0)
			if part<parts:server+=1;parts=0
			else:parts=part
			numserver='S%d'%server if server%2==0 else '[COLOR green]S%d[/COLOR]'%server
			if part==0:label='[COLOR gold]%s %s[/COLOR]: '%(numserver,language)+name;server+=1
			else:
				label='[COLOR gold]%s-part%d-%s[/COLOR]: '%(numserver,part,language)
				label+=re.sub('\[COLOR gold\].{1,5}ph??t\[/COLOR\] - ','',name)
			addir_info(label,i['url'].replace('\\',''),img,art,mode,page,'pmplay_ple')
	elif query=='pmplay_ple':
		href=pm_get_maxlink(url)
		if href:xbmcsetResolvedUrl(href)
		else:mess(u'Kh??ng get ???????c maxspeedlink ho???c link b??? die!','phimmoi.net')
	elif query=='pmplay_pbo':
		href=pm_get_maxlink(xsearch("currentEpisode.url='(.+?)'",make_request(url)))
		if href:xbmcsetResolvedUrl(href)
		else:mess(u'Kh??ng get ???????c maxspeedlink ho???c link b??? die!','phimmoi.net')
	elif query=='pmplay_trailer':
		href=xsearch("filmInfo.trailerUrl='(.+?)'",make_request(url))
		return play_youtube(href)

def phim3s(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phim3s.png');urlhome='http://phim3s.net/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('https://static-s.aa-cdn.net/img/ios/888227595/8efccc86a2a835c412ab46cbf99c3e15',ico)
		except:pass
	
	def namecolor(name):return '%s%s[/COLOR]'%(color['phim3s'],name)
	def namenocolor(n):return xsearch('%s(.+?)\['%color['phim3s'].replace('[','\[').replace(']','\]'),n)
	def login(u='xshare',p='xsharethaitni'):
		hd['X-Requested-With']='XMLHttpRequest';data={'username':u,'password':p}
		try:l=make_post('http://phim3s.net/member/login/',hd,data);cookie=l.cookiestring;l=l.json
		except:l={};cookie=''
		mess(u'%s'%l.get('message',['Login to phim3s.net fail !',''])[0],'Login to Phim3s.net');hd['Cookie']=cookie
		return hd
	
	def clip_getdetail(body):	
		for s in re.findall('(<div class="box">.+?</div>)',body,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			title=xsearch('title="(.+?)"',s)
			img=xsearch('lsrc="(.+?)"',s)
			dur=xsearch('<span class="video-time">(.+?)</span>',s)
			addir_info(title,href,img,img,mode,1,"clip_play")
		pagination=re.search('<a href="[^<]+?">(\d+?)</a></li><li><a href="([^<]+?)">&gt;</a>',body)
		if pagination:
			name=color['trangtiep']+'Trang ti???p theo: trang %d/%s[/COLOR]'%(page+1,pagination.group(1))
			addir_info(name,pagination.group(2),img,'',mode,page+1,'clip_items',True)
	
	if query=='phim3s.net':
		body=get_home_page('phim3s.html',urlhome)
		title=color['search']+"Search tr??n phim3s.net[/COLOR]"
		addir_info(title,'phim3s.net',ico,'',mode,1,'search',True)
		title=color['search']+"H???p phim c???a t??i tr??n phim3s.net[/COLOR]"
		addir_info(title,'http://phim3s.net/ajax/member/get_bookmarks',ico,'',mode,1,'get_bookmark',True)
		
		S=xsearch('(<ul class="container menu">.+?</ul></div>)',body)
		for title in re.findall('<a>(.+?)</a><ul class="sub-menu"',S):
			addir_info(namecolor(title),'',img,img,mode,1,"p3s_menu",True)
		
		i=re.findall('</ul></li><li><h3><a href="(.+?)" title=".*?">(\D+?)</a></h3><ul class="sub-menu"',S)
		for href,title in i:addir_info(namecolor(title),href,img,img,mode,1,"p3s_menu",True)
		i=re.findall('<a href="([^<]+?)" title="[^<]+?">([^<]+?)</a>',S)
		try:
			s=i[len(i)-2];addir_info(namecolor(s[1]),s[0],img,img,mode,1,"p3s_page",True)
			s=i[len(i)-1];addir_info(namecolor(s[1]),s[0],img,img,mode,1,"p3s_page",True)
		except:pass
		
		add_sep_item("------------------------------------")
		addir_info(namecolor('Xem nhi???u nh???t Ng??y/Tu???n/Th??ng'),'tuan',img,img,mode,1,"xemnhieu",True)
		S=xsearch('(<ul class="tab topviewday">.+?</ul>)',body)
		i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S);menu={'bookmark':{'action':'Add'}}
		for href,title in i:
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"get_server",True,menu=menu)
		
		add_sep_item("------------------------------------")
		addir_info('Phim b??? ???? ho??n th??nh','',img,img,mode,1,"")
		S=xsearch('(<ul class="list tab phim-bo-full.+?</ul>)',body)
		i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S)
		
		for href,title in i:
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"get_server",True,menu=menu)
		
		if get_home_page('phim3s.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=="xemnhieu":
		body=get_home_page('phim3s.html')
		if url=='tuan':
			addir_info(namecolor('Xem nhi???u nh???t Th??ng'),'thang',img,img,mode,1,"xemnhieu",True)
			S=xsearch('(<ul class="tab topviewweek.+?</ul>)',body)
		else:S=xsearch('(<ul class="tab topviewmonth.+?</ul>)',body)
		i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S);menu={'bookmark':{'action':'Add'}}
		for href,title in i:
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"get_server",True,menu=menu)
	
	elif query=="p3s_menu":
		body=get_home_page('phim3s.html');name=namenocolor(name)
		if not url:
			S=xsearch('(<a>%s</a><ul class="sub-menu".+?</a></li></ul></li>)'%name,body)
			i=re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S)
			for href,title in [s for s in i if url in s[0]]:
				addir_info(namecolor(title),urlhome+href,img,img,mode,1,"p3s_page",True)
		else:
			S=xsearch('</ul></li><li><h3><a href="%s"(.+?</li></ul>)'%url,body)
			for href,title in re.findall('href="(.+?)" title=".+?">(.+?)</a>',S):
				addir_info(namecolor(title),urlhome+href,img,img,mode,1,"p3s_page",True)
			phim3s(name,url,img,mode,page,'p3s_page')
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phim3s(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phim3s.net":
		search_string = urllib.quote_plus(query)
		url='http://phim3s.net/search/%s'%search_string
		return phim3s(name,url,img,mode,1,query='p3s_page')
	
	elif query=='clip_getpage':
		body=get_home_page('phim3s_clip.html','http://m-viet.com/');c='[COLOR orange]'
		addir_info(c+'Clip[/COLOR]','http://m-viet.com/popular/',img,img,mode,0,"clip_items",True)
		addir_info(c+'Danh m???c[/COLOR]','http://m-viet.com/category/tin-tuc',img,img,mode,0,"clip_items",True)
		clip_getdetail(body)
		if get_home_page('phim3s_clip.html','http://m-viet.com/',True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=='clip_items':
		body=make_request(url);name=xsearch('\](.+?)\[',name)
		if page==0:
			page==1
			if '/category/' in url:
				s=xsearch('(>%s</a>.+?</ul>)'%name,body,1,re.DOTALL)
				pattern='href="(.+?)" title=".+?">(.+?)</a>'
			else:
				s=xsearch('(<li><a title=".+?" href="%s">.+?</ul>)'%url,body,1,re.DOTALL)
				pattern='href="(.+?)">(.+?)</a>'
			for href,title in re.findall(pattern,s):
				if href==url:continue
				addir_info('[COLOR orange]'+title+'[/COLOR]',href,img,img,mode,1,"clip_items",True)
		clip_getdetail(body)
		
	elif query=="clip_play":
		body=make_request(url)
		link=xsearch('src="(http://www.youtube.com/.+?)"',body)
		if link:play_youtube(link)
		
	elif query=='p3s_page':
		if '/m-viet.com/' in url:return phim3s(name,'http://m-viet.com/',img,mode,1,query='clip_getpage')
		if 'http://' not in url:url=urlhome+url
		body=xsearch('(<ul class="list-film">.+?</span></div></div></div></div>)',make_request(url),1,re.DOTALL)
		i=re.findall('<a href="(.+?)".+?img src="(.+?)".+?title="(.+?)".+?class="status">(.+?)</div>',body)
		menu={'bookmark':{'action':'Add'}}
		for href,img,title,res in i:
			title=namecolor(title)
			if res:title+=' [COLOR gold]'+res+'[/COLOR]'
			addir_info(namecolor(title),href,img,img,mode,1,"get_server",True,menu=menu)
			
		i=re.search('<a href="[^<]+?">(\d+?)</a></span><span class="item"><a href="([^<]+?)">Next</a></span>',body)
		if i:
			name=color['trangtiep']+'Trang ti???p theo: trang %d/%s[/COLOR]'%(page+1,i.group(1))
			addir_info(name,i.group(2),img,'',mode,page+1,'p3s_page',True)
			
	elif query=='get_server':
		if 'http://' not in url:url=urlhome+url
		if '/xem-phim/' not in url:url=url+'xem-phim/'
		body=make_request(url);menu={'bookmark':{'action':'Add'}}
		for s in re.findall('(<div class="server">.+?</ul></div>)',body,re.DOTALL):
			server=xsearch('</i>(.+?)</div>',s)
			if server:addir_info(color['trangtiep']+server+'[/COLOR]','',ico,'',mode,1,"")
			for id,href,title in re.findall('data-episode-id="(.+?)" href="(.+?)" title="(.+?)"',s):
				addir_info(re.sub('Server V.I.P.+?- ','',title)+' '+name,urlhome+href,img,'',mode,1,"p3s_play",menu=menu)
	
	elif query=='get_bookmark':
		from resources.lib.servers import phim3s_net
		p3s=phim3s_net(myaddon.getSetting('p3s_u'),myaddon.getSetting('p3s_p'))
		bookmark=p3s.get_bookmark();menu={'bookmark':{'action':'Remove'}}
		for i in bookmark.get('json'):
			bm=bookmark.get('json')[i];href=bm.get('link');img=bm.get('thumb_url')
			title=u2s(bm.get('short_title')+' - '+bm.get('short_title_o'))
			text=bm.get('pagetext');fanart=xsearch('"(http.+?\.jpg)',text)
			if not fanart:fanart=img
			addir_info(namecolor(title),href,img,fanart,mode,1,"get_server",True,menu=menu)
			
	elif query=='add_bookmark' or query=='remove_bookmark':
		from resources.lib.servers import phim3s_net
		p3s=phim3s_net(myaddon.getSetting('p3s_u'),myaddon.getSetting('p3s_p'))
		p3s.action_bookmark(url,query)
		if query=='remove_bookmark':xbmc.executebuiltin("Container.Refresh")

	elif query=='p3s_play':
		import time;hd['X-Requested-With']='XMLHttpRequest';id=xsearch('/(\d+)',url);max_link=''
		href='http://phim3s.net/ajax/episode/embed/?episode_id=%s&_=%d'%(id,int(time.time()*1000))
		j=make_request(href,hd,resp='j')
		#makerequest(r'd:\xoa.html',str(j)+href+str(hd),'w')
		href=j.get('grabber')+'?link='+urllib.quote_plus(j.get('video_url_hash'))+'&json=1'#&s=19'
		l=make_request(href,resp='j')
		if not l:print 'swapping..............';l=make_request(re.sub('http://sub.\.','http://sub4.',href),resp='j')
		
		if l:
			#print json.dumps(l,indent=2,ensure_ascii=True)
			L=[(s.get('file'),resolu(s.get('label'))) for s in l]
			#print L
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			for href,label in L:
				max_link=dl(href)
				if max_link:break
		
		if not max_link:
			videoUrl=xsearch("videoUrl = '(.+?)'",make_request(url))
			if videoUrl:max_link=dl(href)
		
		if max_link:xbmcsetResolvedUrl(max_link)
		else:mess('No playable source found!','phim3s.net')
	
def kenh88(name,url,img,mode,page,query):
	color['kenh88']='[COLOR cyan]';ico=os.path.join(iconpath,'kenh88.png');urlhome='http://www.kenh88.com/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://www.kenh88.com/images/logo_kenh88.png',ico)
		except:pass
	def namecolor(name):return '%s%s[/COLOR]'%(color['kenh88'],name)
	def get_detail(s):
		tap=xsearch('class="process">T???p <p>(.+?)</p></span>',s)
		if not tap:tap=xsearch('class="process_r">(.+?)</span>',s)
		res=xsearch('<span class="status">(.+?)</span>',s)
		href='%sxem-phim-online/%s'%(urlhome,os.path.basename(xsearch('href="/(.+?)"',s)))
		title=xsearch('href=".+?">([^<].+?)</a>',s)+'-'+xsearch('href=".+?">.+?</a>(.+?)</h2>',s)
		title=' '.join(title.split())
		if res:title+='[COLOR blue]-%s[/COLOR]'%res
		if tap:title+='[COLOR gold]-%s[/COLOR]'%tap
		img=urlhome+xsearch('src="/(.+?)"',s)
		return tap,href,title,img
	def get_maxlink(url):
		response=make_request(url,resp='o');max_link='';width=0
		if response and response.status==200:
			link=xsearch('proxy.link=(.+?)&',response.body)
			if 'dailymotion' in link:
				body=make_request(link)
				data=xsearch('"qualities"\:(.+?\}\]\}),',body)
				try:data=json.loads(data)
				except:data={}
				for d in data:
					try:
						detail=data.get(d)[0]
						if 'video' in detail.get('type') and int(d)>width:
							width=int(d);max_link=detail.get('url')
					except:pass
			elif 'www.youtube.com' in link:max_link=link
			elif 'phimhub.com' in link:max_link=link
			elif 'drive.google.com' in link:
				link=link.split('*')[0]
				body=make_request(link,maxr=3)
				urls_encoded=xsearch('(\["url_encoded_fmt_stream_map",".+?\])',body)
				try:urls_encoded=urllib.unquote(eval(urls_encoded)[1])+','
				except:urls_encoded=''
				for href,q in re.findall('(https.+?)\\\(.+?quality.+?),',urls_encoded):
					if 'video' in q:
						if '1080' in q:max_link=href;width=1
						elif '720' in q and not width:max_link=href;width=1
						elif not width:max_link=href
			else:
				data=make_post('http://www.kenh88.com/media/plugins/plugins_player.php',data={'url':link})
				try:data=json.loads(xsearch('(\[.+?\])',data.body))
				except:data={}
				for d in data:
					try:
						if 'video' in d.get('type') and int(d.get('width'))>width:
							width=int(d.get('width'));max_link=d.get('url')
					except:pass
		return max_link

	if query=='kenh88.com':
		body=get_home_page('kenh88.html',urlhome)
		title=color['search']+"Search tr??n kenh88.com[/COLOR]"
		addir_info(title,'kenh88.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Xem nhi???u nh???t'),'',img,img,mode,1,"xemnhieu",True)
		menu=re.findall('<a title="(.+?)"[\s| ].*?href="(.+?)"[\s| ].+?class=".+?">',body)
		for title,href in menu:
			if title=='Home':continue
			elif 'javascript' in href:
				addir_info(namecolor(title),'',img,img,mode,1,"k88_menu",True)
			else:
				href=urlhome+href.replace('/','')
				addir_info(namecolor(title),href,img,img,mode,1,"k88_getpage",True)
		addir_info('%s%s[/COLOR]'%(color['trangtiep'],'-----------------------------'),'',img,img,mode,1,"")
		for S in re.findall("(<div class=''.+?/h2>)",body,re.DOTALL):
			tap,href,title,img=get_detail(S)
			addir_info(namecolor(title),href,img,img,mode,1,"k88_getpage",True)
		if get_home_page('kenh88.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return kenh88(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="kenh88.com":
		search_string = urllib.quote_plus(query)
		url='http://www.kenh88.com/film/search?keyword=%s'%search_string
		return kenh88(name,url,img,mode,1,query='k88_getpage')
	elif query=='k88_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('(<a title="%s".+?/ul>)'%loai,get_home_page('kenh88.html'),1,re.DOTALL)
		for href,title in re.findall('href="/(.+?)">(.+?)</a>',S):
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"k88_getpage",True)
	elif query=='k88_getpage':
		body=make_request(url);name=xsearch('\](.+?)\[',name)
		items=re.findall('(class="server".+?</ul>)',body,re.DOTALL)
		if items:
			for S in items:
				s=xsearch('</i>(.+?)</div>',S)
				if s:addir_info('%s%s[/COLOR]'%(color['trangtiep'],s),'',img,img,mode,1,"")
				for  href,title in re.findall('<a href="/(.+?)"\s.+?>(.+?)</a>',S):
					addir_info('T???p %s - %s'%(title,name),urlhome+href,img,'',mode,1,"k88_play")
		else:
			items=re.findall("(<div class=''.+?<h2>.+?</div>)",body,re.DOTALL)
			for S in items:
				tap,href,title,img=get_detail(S)
				addir_info(namecolor(title),href,img,img,mode,1,"k88_getpage",True)
		href=xsearch('class="next" href="/(.+?)\?',body)
		if href:
			pages=xsearch('>(\d{,4})</a></li><li><span>',body)
			title=namecolor(name)+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,urlhome+href,ico,'',mode,page+1,query,True)
	elif query=='xemnhieu':		
		body=get_home_page('kenh88.html');top={'1':'TOP Ng??y','2':'TOP Tu???n','3':'TOP Th??ng'}
		for S in re.findall('("sidebarlist-(\d)">.+?div id)',body,re.DOTALL):
			addir_info(color['trangtiep']+top.get(S[1])+'[/COLOR]','',img,img,mode,1,"")
			for href,title,img in re.findall('<a href="/(.+?)"><img alt="(.+?)" src="/(.+?)"',S[0]):
				href='%sxem-phim-online/%s'%(urlhome,os.path.basename(href))
				addir_info(namecolor(title),href,urlhome+img,urlhome+img,mode,1,"k88_getpage",True)
	elif query=='k88_play':
		response=make_request(url)
		#makerequest(r'd:\xoa.html',response,'w')
		link=xsearch('\{link:.*"(.+?)"\}',response)
		if len(link)>20:
			jp=make_post('http://www.kenh88.com/gkphp/plugins/gkpluginsphp.php',data={'link':link},resp='j')
			label=0;link='';j=jp.get('link')
			if isinstance(j,dict):
				for l in j.get('link'):
					l1=int(xsearch('(\d+)',l.get('label'),result=0))
					if l1>label:label=l1;link=l.get('link')
			if isinstance(j,list):
				for l in j:
					l1=int(xsearch('(\d+)',l.get('label'),result=0))
					if l1>label:label=l1;link=l.get('link')
			elif isinstance(j,unicode):link=j
			elif jp.get('error'): mess(jp.get('error'),'Kenh88.com')
			if link:
				s=make_request(link,resp='o',maxr=3)
				try:link=s.history[-1].headers['location']
				except:pass#link=''
				if link:xbmcsetResolvedUrl(link)
				else:mess('File invalid or deleted!','Kenh88.com') 
		elif xsearch('src="(.+?docid=.+?)"',response):
			docid=xsearch('docid=(.+?)&',response)
			if docid:
				link='https://docs.google.com/get_video_info?authuser=&eurl=%s&docid=%s'
				link=link%(urllib.quote_plus(url),docid)
				response=make_request(link)
				link=xsearch('url_encoded_fmt_stream_map(.+?)\Z',response)
				link=xsearch('url=(.+?)&type=',urllib.unquote(urllib.unquote(link)))
				
				xbmcsetResolvedUrl(link)
		else:mess('No playable sources found !','Kenh88.com')
			
	elif query=='k88_play1':
		max_link=get_maxlink(url)
		if max_link and  'www.youtube.com' in max_link:play_youtube(max_link)
		elif max_link:xbmcsetResolvedUrl(max_link)
		else:mess('File invalid or deleted!','Kenh88.com') 

def phimdata(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phimdata.png');urlhome='http://www.phimdata.com/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://www.phimdata.com/images/logo_kenh88.png',ico)
		except:pass
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimdata'],name)
	def get_detail(s):
		tap=xsearch('class="process">T???p <p>(.+?)</p></span>',s)
		if not tap:tap=xsearch('class="process_r">(.+?)</span>',s)
		res=xsearch('<span class="status">(.+?)</span>',s)
		href='%scoi-phim-online/%s'%(urlhome,os.path.basename(xsearch('href="/(.+?)"',s)))
		title=xsearch('href=".+?">([^<].+?)</a>',s)+'-'+xsearch('href=".+?">.+?</a>(.+?)</h2>',s)
		title=' '.join(title.split())
		if res:title+='[COLOR blue]-%s[/COLOR]'%res
		if tap:title+='[COLOR gold]-%s[/COLOR]'%tap
		img=urlhome+xsearch('src="/(.+?)"',s)
		return tap,href,title,img
	def get_maxlink(body):
		link=xsearch('proxy.link=(.+?)&',body);max_link='';width=0
		if 'dailymotion' in link:
			body=make_request(link)
			data=xsearch('"qualities"\:(.+?\}\]\}),',body)
			try:data=json.loads(data)
			except:data={}
			for d in data:
				try:
					detail=data.get(d)[0]
					if 'video' in detail.get('type') and int(d)>width:
						width=int(d);max_link=detail.get('url')
				except:pass
		elif 'www.youtube.com' in link:max_link=link
		elif 'phimhub.com' in link:max_link=link
		elif 'drive.google.com' in link:
			link=link.split('*')[0]
			body=make_request(link,maxr=3)
			urls_encoded=xsearch('(\["url_encoded_fmt_stream_map",".+?\])',body)
			try:urls_encoded=urllib.unquote(eval(urls_encoded)[1])+','
			except:urls_encoded=''
			for href,q in re.findall('(https.+?)\\\(.+?quality.+?),',urls_encoded):
				if 'video' in q:
					if '1080' in q:max_link=href;width=1
					elif '720' in q and not width:max_link=href;width=1
					elif not width:max_link=href
		else:
			data=make_post('http://www.phimdata.com/media/plugins/plugins_player.php',data={'url':link})
			try:data=json.loads(xsearch('(\[.+?\])',data.body))
			except:data={}
			for d in data:
				try:
					if 'video' in d.get('type') and int(d.get('width'))>width:
						width=int(d.get('width'));max_link=d.get('url')
				except:pass
		return max_link

	if query=='phimdata.com':
		body=get_home_page('phimdata.html',urlhome)
		title=color['search']+"Search tr??n phimdata.com[/COLOR]"
		addir_info(title,'phimdata.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Xem nhi???u nh???t'),'',img,img,mode,1,"xemnhieu",True)
		menu=re.findall('<a title="(.+?)"[\s| ].*?href="(.+?)"[\s| ].+?class=".+?">',body)
		for title,href in menu:
			if title=='Home':continue
			elif 'javascript' in href:
				addir_info(namecolor(title),'',img,img,mode,1,"pdt_menu",True)
			else:
				href=urlhome+href.replace('/','')
				addir_info(namecolor(title),href,img,img,mode,1,"pdt_getpage",True)
		addir_info('%s%s[/COLOR]'%(color['trangtiep'],'-----------------------------'),'',img,img,mode,1,"")
		for S in re.findall("(<div class=''.+?/h2>)",body,re.DOTALL):
			tap,href,title,img=get_detail(S)
			addir_info(namecolor(title),href,img,img,mode,1,"pdt_getpage",True)
		if get_home_page('phimdata.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimdata(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phimdata.com":
		search_string = urllib.quote_plus(query)
		url='http://www.phimdata.com/film/search?keyword=%s'%search_string
		return phimdata(name,url,img,mode,1,query='pdt_getpage')
	elif query=='pdt_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('(<a title="%s".+?/ul>)'%loai,get_home_page('phimdata.html'),1,re.DOTALL)
		for href,title in re.findall('href="/(.+?)">(.+?)</a>',S):
			addir_info(namecolor(title),urlhome+href,img,img,mode,1,"pdt_getpage",True)
	elif query=='pdt_getpage':
		body=make_request(url);name=xsearch('\](.+?)\[',name)
		items=re.findall('(class="server".+?</ul>)',body,re.DOTALL)
		if items:
			for S in items:
				s=xsearch('</i>(.+?)</div>',S)
				if s:addir_info('%s%s[/COLOR]'%(color['trangtiep'],s),'',img,img,mode,1,"")
				for  href,title in re.findall('<a href="/(.+?)"\s.+?>(.+?)</a>',S):
					addir_info('T???p %s - %s'%(title,name),urlhome+href,img,'',mode,1,"pdt_play")
		else:
			items=re.findall("(<div class=''.+?<h2>.+?</div>)",body,re.DOTALL)
			for S in items:
				tap,href,title,img=get_detail(S)
				addir_info(namecolor(title),href,img,img,mode,1,"pdt_getpage",True)
		href=xsearch('class="next" href="/(.+?)\?',body)
		if href:
			pages=xsearch('>(\d{,4})</a></li><li><span>',body)
			title=namecolor(name)+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,urlhome+href,ico,'',mode,page+1,query,True)
	elif query=='xemnhieu':		
		body=get_home_page('phimdata.html');top={'1':'TOP Ng??y','2':'TOP Tu???n','3':'TOP Th??ng'}
		for S in re.findall('("sidebarlist-(\d)">.+?div id)',body,re.DOTALL):
			addir_info(color['trangtiep']+top.get(S[1])+'[/COLOR]','',img,img,mode,1,"")
			for href,title,img in re.findall('<a href="/(.+?)"><img alt="(.+?)" src="/(.+?)"',S[0]):
				href='%scoi-phim-online/%s'%(urlhome,os.path.basename(href))
				addir_info(namecolor(title),href,urlhome+img,urlhome+img,mode,1,"pdt_getpage",True)
	elif query=='pdt_play':
		response=make_request(url)
		max_link=get_maxlink(response)
		if max_link and  'www.youtube.com' in max_link:play_youtube(max_link)
		elif max_link:xbmcsetResolvedUrl(max_link)
		else:
			link=xsearch('\{link:.*"(.+?)"\}',response)
			if len(link)>20:
				jp=make_post('http://www.phimdata.com/gkphp/plugins/gkpluginsphp.php',data={'link':link},resp='j')
				label=0;link='';j=jp.get('link')
				if isinstance(j,dict):
					for l in j.get('link'):
						l1=int(xsearch('(\d+)',l.get('label'),result=0))
						if l1>label:label=l1;link=l.get('link')
				if isinstance(j,list):
					for l in j:
						l1=int(xsearch('(\d+)',l.get('label'),result=0))
						if l1>label:label=l1;link=l.get('link')
				elif isinstance(j,unicode):link=j
				elif jp.get('error'): mess(jp.get('error'),'phimdata.com')
				if link:
					s=make_request(link,resp='o',maxr=3)
					try:link=s.history[-1].headers['location']
					except:pass#link=''
					if link:xbmcsetResolvedUrl(link)
					else:mess('File invalid or deleted!','phimdata.com') 
			elif xsearch('src="(.+?docid=.+?)"',response):
				docid=xsearch('docid=(.+?)&',response)
				if docid:
					link='https://docs.google.com/get_video_info?authuser=&eurl=%s&docid=%s'
					link=link%(urllib.quote_plus(url),docid)
					response=make_request(link)
					link=xsearch('url_encoded_fmt_stream_map(.+?)\Z',response)
					link=xsearch('url=(.+?)&type=',urllib.unquote(urllib.unquote(link)))
					xbmcsetResolvedUrl(link)
			else:mess('No playable sources found !','phimdata.com')

def phimsot(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phimsot.png');urlhome='http://phimsot.com/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://phimsot.com/default/template/img/icon_200x200.png',ico)
		except:pass
	def namecolor(name):return '%s%s[/COLOR]'%(color['phimsot'],name)
	def get_detail(s):
		tap=xsearch('class="process"><span>(.+?)</span>',s)
		res=xsearch('<br>Ch???t l?????ng: <b>(.+?)</b>',s)
		href=xsearch('href="(.+?)"',s)
		title=xsearch('alt="(.+?)"',s)
		title=' '.join(title.split())
		sub=xsearch('<br>Chuy???n ng???: <b>(.+?)</b>',s)
		if res:title+='[COLOR blue]-%s[/COLOR]'%res
		if tap:title+='[COLOR gold]-%s[/COLOR]'%tap
		if sub:title+='[COLOR blue]-%s[/COLOR]'%sub
		img=xsearch('src="(.+?)"',s)
		return tap,href,title,img
	
	def get_maxlink(url,loop=False):
		body=make_request(url);quality=0;max_link=picasa=sub='';found=False;srvs=[]
		for url in re.findall('href="(http://phimsot.com/xem-online.+?)"',body):
			if url in srvs:continue
			else:srvs.append(url)
			content=make_request(url)
			for link in re.findall("'playlist': '(.+?)'",content):
				response=make_request(link)
				for href,q in re.findall('file="(.+?)" label="(\d.+?)"',response):
					if int(xsearch('(\d{,4})',q))>quality:quality=int(xsearch('(\d{,4})',q));picasa=href
				if picasa:
					sub=xsearch('file="(.+?)" label=".+?" kind="captions"',response)
					s=make_request(picasa,resp='o',maxr=3)
					try:max_link=s.history[-1].headers['location'];break
					except:pass
			if max_link:break
		if not max_link and not loop:
			loop=True
			for srv in [s for s in re.findall('class="left server_name">.+?<a href="(.+?)"',content) if s not in srvs]:
				max_link,sub=get_maxlink(srv,True)
				if max_link:break
			return max_link,sub
		return max_link,sub
	
	def ps_getpage(body):
		for S in re.findall('(<div class="film_short">.+?class="subname".+?</div>)',body,re.DOTALL):
			tap,href,title,img=get_detail(S)
			if 'Info' in tap or 'trailer' in tap:continue
			if tap:title+=' [COLOR gold]%s[/COLOR]'%tap
			addir_info(namecolor(title),href,img,img,mode,1,'get_series',True)
		S=xsearch('(<div class="paging">.+?</div>)',body,1,re.DOTALL)
		next=xsearch('(class="ajax_select paging_active" href=".+?">.+?</a>\s\s.+?<a class="ajax_select" href=".+?">.+?</a>)',S)
		#print S,next
		if S and next:
			page_next=xsearch('class="ajax_select" href=".+?">(.+?)</a>',next)
			href_next=xsearch('class="ajax_select" href="(.+?)">.+?</a>',next)
			title=namecolor(xsearch('\](.+?)\[',name))
			title=title+color['trangtiep']+' Trang tiep theo...trang %s[/COLOR]'%page_next
			addir_info(title,href_next,ico,'',mode,int(page_next),'ps_getpage',True)

	if query=='phimsot.com':
		body=get_home_page('phimsot.html',urlhome)
		title=color['search']+"Search tr??n phimsot.com[/COLOR]"
		addir_info(title,'phimsot.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Top 1 Movie'),'http://vi.top1movie.com',img,img,mode,1,"top1movie",True)
		for href,title in re.findall('<li>\s.+?<a.+?href="(.+?)" title=".+?">([^<].+?)</a>',body):
			addir_info(namecolor(title),'',img,img,mode,1,"ps_menu",True)
		addir_info('%s%s[/COLOR]'%(color['trangtiep'],'-----------------------------'),'',img,img,mode,1,"")
		ps_getpage(body)
		if get_home_page('phimsot.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimsot(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phimsot.com":
		search_string = urllib.quote_plus(query)
		url='http://phimsot.com/phim-hay-p1/?keyword=%s'%search_string
		return phimsot(name,url,img,mode,1,query='ps_getpage')
	
	elif query=='ps_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('(title="%s">%s</a>.+?</ul>)'%(loai,loai),get_home_page('phimsot.html'),1,re.DOTALL)
		for href,title in re.findall('<a class=".+?" href="(.+?)" title=".+?">(.+?)</a>',S):
			addir_info(namecolor(title),href,img,img,mode,1,"ps_getpage",True)
	
	elif query=='top1movie':	
		def detail(s):
			href=xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('alt="(.+?)"',s)
			alert=xsearch('"alert alert-warning comment">(.+?)</div>',s)
			epi=xsearch('>(.{,4})</a>/.{,10}</strong></span>',s)
			eps=xsearch('>.{,4}</a>/(.{,10})</strong></span>',s)
			return title,href,img,epi,eps,alert
		body=make_request(url);S=''
		for S in re.findall('(<div class="col-md-6">.+?</div> </div> </div>)',body,re.DOTALL):
			title,href,img,epi,eps,alert=detail(S)
			if epi or eps:title+=' [COLOR gold]%s/%s[/COLOR]'%(epi,eps)
			if alert:title+=' [COLOR green]%s[/COLOR]'%alert
			addir_info(namecolor(title),href,img,img,mode,1,"top1movie_series",True)
		if S:
			page+=1;title=color['trangtiep']+'Top1Movie trang %d[/COLOR]'%page
			addir_info(title,'http://vi.top1movie.com/?page=%d'%page,img,img,mode,page,'top1movie',True)
	
	elif query=='top1movie_series':
		body=make_request(url);fanart=xsearch('<meta property="og:image" content="(.+?)"',body)
		s=xsearch('(<ul class="dropdown-menu scrollable-select".+?</ul>)',body,1,re.DOTALL)
		for href,title in reversed(re.findall('<a href="(.+?)">(.+?)</a>',s)):
			addir_info(title,href,img,fanart,mode,1,'top1movie_play')
	
	elif query=='top1movie_play':
		body=make_request(url+'&quality=HD');max_link=''
		link=xsearch('<source src="(.+?)"',body)
		try:max_link=make_request(link,resp='o',maxr=3);max_link= max_link.history[-1].headers['location']
		except:pass
		if max_link:
			sub=xsearch('<track src="(.+?)" kind="subtitles" srclang="vi"',body)
			if not sub:sub=xsearch('<track src="(.+?)" kind="subtitles" srclang="en"',body)
		xbmcsetResolvedUrl(max_link)
		if sub:xbmc.sleep(1000);xbmc.Player().setSubtitles(sub)
		
	elif query=='ps_getpage':ps_getpage(make_request(url))
	elif query=='get_series':
		name=xsearch('\](.+?)\[',name);url=os.path.dirname(url)+os.path.basename(url)+'e0'
		body=make_request(url.replace('/phim/','/xem-phim/'))
		#body=make_request(xsearch('class="button button_20px" href="(.+?)"',body))
		S=xsearch('(<h4 class="server_name">.+?<div class="clear">)',body,1,re.DOTALL)
		for s in S.splitlines():
			title=xsearch('<h4 class="server_name">(.+?)</h4>',s)
			if title:addir_info('%s%s[/COLOR]'%(color['trangtiep'],title),'',img,'',mode,1,"");continue
			if ' <a class=' in s:
				href=xsearch('href="(.+?)"',s)
				title=xsearch('title="(.+?)"',s)
				tap=xsearch('>(.+?)</a>',s)
				addir_info(tap+' - '+title,href,img,'',mode,1,'ps_play')
	
	elif query=='ps_play':
		body=make_request(url);quality=''
		for href,q in re.findall('<a class="go_episode" href="(.+?)" download title="Download .+?">(.+?)</a>',body):
			if q>quality:quality=q;link=href
		if quality:
			link=make_request(link,resp='o',maxr=3)
			try:link=link.history[-1].headers['location'];xbmcsetResolvedUrl(link)
			except:link=''
		else:
			link=xsearch('id="mainPayler".+?\s.+?\s.+?src="(.+?)"',body)
			if 'youtube.com' in link:play_youtube(link)
			elif link:
				link=make_request(link,resp='o',maxr=3)
				try:link=link.history[-1].headers['location'];xbmcsetResolvedUrl(link)
				except:pass
			#if sub:xbmc.sleep(1000);xbmc.Player().setSubtitles(sub)
			else:mess('File invalid or deleted!','phimsot.com') 

def phim47(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phim47.png');urlhome='http://phim47.com/';c='springgreen'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://tailieuhot.vn/images/danh-ba-web/phim-47.jpg',ico)
		except:pass
	def namecolor(name):return '%s%s[/COLOR]'%(color['phim47'],name)
	def get_detail(s):
		tm=xsearch('(<span class="thuyetminh">)',s) or xsearch('(title="Audio Vi???t")',s)
		series=xsearch('class="bo">(.*?)</span>',s)
		views=xsearch('"viewshow">(.*?)</span>',s)
		href=xsearch('<a href="(.+?)"',s)
		title=xsearch('alt="(.+?)"',s)
		img=xsearch('src="(.+?)"',s)
		return title,href,img,tm,series,views
	def get_items(content):
		items=re.findall('(class="zitemList.+?class="menuTitle)',content,re.DOTALL)
		if not items:items=re.findall('(<div class="imgnh left">.+?<div class=.clear_tdno.>)',content,re.DOTALL)
		for S in items:
			title,href,img,tm,series,views=get_detail(S)
			if tm:title=title+' [COLOR gold]TM[/COLOR]'
			if views:title+=' %s '%views
			if series:title+='[COLOR gold]%s[/COLOR]'%series
			if 'http://' not in href:href=urlhome+href 
			addir_info('[COLOR darkseagreen]'+title+'[/COLOR]',href,img,img,mode,1,'get_series',True)
	
	if query=='phim47.com':
		body=get_home_page('phim47.html',urlhome)
		title=color['search']+"Search tr??n phim47.com[/COLOR]"
		addir_info(title,'phim47.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Xem nhi???u nh???t'),'',img,img,mode,1,"xemnhieu",True)
		for s,title in re.findall('<li class="downmenu"><span><a(.+?)>(.+?)</a></span>',body):
			if 'onmouseover' in s:addir_info(namecolor(title),'',img,img,mode,1,"p47_menu",True)
			else:addir_info(namecolor(title),xsearch('href="(.+?)"',s),img,img,mode,1,"p47_getpage",True)
		addir_info('%s%s[/COLOR]'%(color['trangtiep'],'-----------------------------'),'',img,img,mode,1,"")
		get_items(body)
		if get_home_page('phim47.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="phim47.com" or query=="INP":
		if query=="INP":query=make_mySearch('',url,'','','','Input')
		if not query:return 'no'
		url='http://phim47.com/tim-kiem/%s.html'%urllib.quote_plus(query)
		return phim47(name,url,img,mode,1,query='p47_getpage')
	
	elif query=='p47_menu':
		loai=xsearch('\](.+?)\[',name)
		S=xsearch('((>%s</a></span><ul class="shownav">.+?</ul></li>))'%loai,get_home_page('phim47.html'),1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)" title=".+?">(.+?)</a>',S):
			addir_info(namecolor(title),href,img,img,mode,1,"p47_getpage",True)
	
	elif query=='xemnhieu':
		from resources.lib.servers import phim47com;p47=phim47com(c)
		for title,href,img in p47.xemnhieu(get_home_page('phim47.html')):
			addir_info(title,href,img,img,mode,1,"get_series",True)
	
	elif query=='xemnhieu':		
		body=get_home_page('phim47.html')
		items=re.findall('<li class="zitem">.+?src="(.+?)".+?<a href="(.+?)".+?>(.+?)</a>',body,re.DOTALL)
		for img,href,title in items:
			addir_info(title,href,img,img,mode,1,"p47_play")
	
	elif query=='p47_getpage':
		body=make_request(url);name=xsearch('\](.+?)\[',name)
		get_items(body)
		pages=xsearch('class=page_text>Page(.+?)</span>',body)
		if pages:
			pages=pages.split('/')
			page_current=int(pages[0]);page_last=int(pages[1]) if len(pages)>1 else 0
			href=xsearch('<span class="click">.+?</span><span class="giua"><a href="(.+?)">',body)
			if href:
				title=namecolor(name)+color['trangtiep']+' Trang tiep theo...trang %d/%d[/COLOR]'%(page+1,page_last)
				addir_info(title,urlhome+href,ico,'',mode,page+1,query,True)
	
	elif query=='get_series':
		name=xsearch('\](.+?)\[',name)
		b=xread(url)
		fanart=xsearch('<link rel="image_src" href="(.+?)"',b);count=0
		for url in re.findall('id="xemphimus" href="(http://phim47.com.+?)"',b):
			b=xread(url);count+=1
			for s in re.findall('("list_episode".+?"clear_span")',b,re.DOTALL):
				title=xsearch('"name_server">([^<]+?)</span>',s)
				if title:add_sep_item('%s-%d----------------------------------------------'%(title,count))
				tap1=xsearch('class="current">([^<]+?)</',s)
				if tap1:addir_info('T???p %s'%tap1+' '+name,url,img,fanart,mode,1,'p47_play')
				for href,title in re.findall('<a href="(.+?)" title="(.+?)">',s):
					addir_info(title+' '+name,href,img,fanart,mode,1,'p47_play')
	
	elif query=='get_series':
		name=xsearch('\](.+?)\[',name)
		body=make_request(url)
		url=xsearch('href="(http://phim47.com/xem-online[^"]+?)"',body);print url
		fanart=xsearch('<link rel="image_src" href="(.+?)"',body)
		body=make_request(xsearch('href="(http://phim47.com/xem-online[^"]+?)"',body))
		for s in re.findall('("list_episode".+?"clear_span")',body,re.DOTALL):
			title=xsearch('"name_server">([^<]+?)</span>',s)
			if title:addir_info('%s%s[/COLOR]'%(color['trangtiep'],title),'',img,fanart,mode,1,"")
			tap1=xsearch('class="current">([^<]+?)</',s)
			if tap1:addir_info('T???p %s'%tap1+' '+name,url,img,fanart,mode,1,'p47_play')
			for href,title in re.findall('<a href="(.+?)" title="(.+?)">',s):
				addir_info(title+' '+name,href,img,fanart,mode,1,'p47_play')
	
	elif query=='p47_play':
		from resources.lib.servers import phim47com;p47=phim47com(c)
		link,sub=p47.getLink(url)
		if link and 'youtube.com' not in link:
			if sub:
				s=xread(sub)
				sub=joinpath(subsfolder,'phim47-Vie.sub')
				makerequest(sub,s,'wb')
			xbmcsetResolvedUrl(link,sub)
		elif link:play_youtube(link)
		else:mess('File invalid or deleted!','phim47.com') 
		
	elif query=='p47_play':
		items=[];link=sub='';items=[];url=url.replace('xem-phim-','xem-online/')
		print url
		from resources.lib.servers import phim47com;p47=phim47com(c)
		for link in re.findall("playlist':.?'(.+?)'",xread(url)):
			l,sub=p47.maxLink(link)
			link=dl(l[0][0])
			if link:break
			else:items+=[i for i in l if link not in i]
		
		if not link:#test all
			mess('Checking all ...','phim47.com')
			if myaddon.getSetting('resolut')=='Max':
				items=sorted(list(set([(i[0],resolu(i[1])) for i in items])), key=lambda k: int(k[1]),reverse=True)
			else:items=sorted(list(set([(i[0],resolu(i[1])) for i in items])), key=lambda k: int(k[1]))
			for href,label in items:
				link=dl(href)
				if link:break
		
		if link:
			xbmcsetResolvedUrl(link)
			if sub:xbmc.sleep(2000);xbmc.Player().setSubtitles(sub);mess(u'Sub c???a phim47.com')
		else:mess('File invalid or deleted!','phim47.com') 

def hdonline(name,url,img,fanart,mode,page,query,bakName,bakData):
	ico=os.path.join(iconpath,'hdonline.png');urlhome='http://hdonline.vn'
	c=xsearch('\[COLOR (\w+)\]',color['hdonline'])
	if not os.path.isfile(ico):
		try:
			link='http://hdonline.vn/template/frontend/images/facebooksharehomepage.png'
			f=open(ico,'wb');f.write(make_request(link));f.close()
		except:pass
	
	def url_fix(url):return url if 'http://' in url else urlhome+url
	def login():
		url='http://id.hdonline.vn/dang-nhap.html'
		primaryKey=xsearch('value="(.+?)" id="primaryKey"',xread(url))
		u=myaddon.getSetting('hdo_u');p=myaddon.getSetting('hdo_p')
		data={'username':u,'password':p,'primaryKey':primaryKey}
		response=make_post(url,data=data)
		if response and response.status==302:
			cookie=response.cookiestring;mess(u'Login to hdonline.vn success')
			hd={'User-Agent':'Mozilla/5.0','Cookie':cookie,'Referer': 'http://hdonline.vn'}
			body=make_request('http://id.hdonline.vn/thong-tin.html',hd)
			userID='; userID=%s'%xsearch('<span class="upgradeVip"><strong>(.+?)</strong>',body)
			makerequest(joinpath(xsharefolder,'hdonline.cookie'),cookie+userID,'w')
		else:cookie='';mess(u'Login to hdonline.vn Fail !')
		return cookie
	
	def page_detail(url):
		items=[]
		for title,href,img,q,dir in hdo.page(url):
			if 'Trang tiep theo...' not in title:
				addir_info(title,href,img,'',mode,1,q,dir,menu=menu)
				items.append((title,href,img,'',mode,1,q,dir,menu))
			else:
				addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
				items.append((title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True,{}))
		return items
	
	if checkupdate('hdonline.cookie',hours=100,folder=xsharefolder):login()
	from resources.lib.servers import hdonline;hdo=hdonline(c)
	hd=hdo.hd;menu={'hdonline':{'action':'Add'}}
	
	if query=='hdonline.vn':
		body=get_home_page('hdonline.html','http://m.hdonline.vn/danh-sach/phim-moi.html',False,hd)
		title=color['search']+"Search tr??n hdonline.vn[/COLOR]"
		addir_info(title,'hdonline.vn',ico,'',mode,1,'search',True)
		title=color['search']+"M???c Y??u th??ch c???a t??i[/COLOR]"
		href='http://hdonline.vn/frontend/user/ajax?page=1&type=like&user=%s'%hdo.userID
		addir_info(title,href,ico,'',mode,1,'like',True)
		
		S=xsearch('(<a href="[^"]+?"><i class="fa fa-film">.+?class="nav")',body,1,re.DOTALL)
		for href,title in re.findall('<a href="([^"]+?)".+class="fa fa-.+>([^<]+?)</a>',S):
			addir_info(namecolor(title,c),href,ico,'',mode,1,"menu",True)
		
		add_sep_item('-------------Phim M???i C???p Nh???t--------------')
		page_detail(body)
		
		if get_home_page('hdonline.html','http://m.hdonline.vn/danh-sach/phim-moi.html',True):
			xbmc.executebuiltin("Container.Refresh")
	
	elif query=='Add':
		id_film=xsearch('-(\d+?)\.html',url)
		body=make_request('http://hdonline.vn/frontend/user/ajax?page=1&type=like&user=%s'%hdo.userID,hdo.hd)
		if xsearch('("#phim-like-%s")'%id_film,body):
			mess(u'Phim n??y ???? c?? trong Danh s??ch Phim y??u th??ch c???a b???n !')
		else:hdo.like_film('http://hdonline.vn/episode/like?film=%s&_=%d'%(id_film,int(time.time())*1000))
	
	elif query=='Remove':
		id_film=xsearch('-(\d+?)\.html',url)
		url='http://hdonline.vn/episode/like?film=%s&_=%d'%(id_film,int(time.time())*1000)
		hdo.like_film(url);xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="hdonline.vn" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		search_string = '-'.join(query.split());page=1;query='page'
		url='http://m.hdonline.vn/tim-kiem/%s/trang-1.html'%search_string;page_detail(url)
	
	elif query=='like':
		b=xread(url);menu={'hdonline':{'action':'Remove'}}
		items=re.findall('(<div class="tn-bxitem">.+?</div>\W</div>)',b,re.S)
		for s in items:
			title,href,img,q,dir=hdo.getDetail(s)
			addir_info(title,url_fix(href),img,'',mode,1,'play',menu=menu)
	
	elif query=='hdo_folder0':#http://hdonline.vn/frontend/video/morevideo?film=12331&_=1465175662582
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		for epi,id in hdo.eps(url):
			print id
			title='T???p %s %s'%(epi,namecolor(name))
			addir_info(title,id,img,'',mode,1,'play')

	elif query=="menu":
		b=xread(url)
		if [s for s in ['M???i','L???','B???'] if s in name]:
			s=xsearch('(<a href="%s".+?</ul>)'%url,b,1,re.DOTALL)
			for href,title in re.findall('<a href="(.+?)" title=.+?</i>(.+?)</a>',s):
				addir_info(namecolor(title,c),href,ico,'',mode,1,"page",True)
			add_sep_item('---------------------------------------')
		
		page_detail(b)
	
	elif query=='eps':
		if 'C??c t???p ti???p theo' in  name:name= url.split('.html')[1];url= url.split('.html')[0]+'.html'
		else:name=namecolor(name)
		id=xsearch('-(\d+)\.html',url)
		for href,epi in hdo.eps(id,page):
			if 'C??c t???p ti???p theo' in href:addir_info(href,url+name,img,'',mode,page+1,query,True)
			else:
				title='T???p-'+epi+' '+name
				addir_info(title,href,img,'',mode,1,'play',menu=menu)
	
	elif query=='eps':
		for title,href,img in hdo.eps(url):
			title=u2s(title)+' '+namecolor(name)
			addir_info(title,href,img,'',mode,1,'play',menu=menu)
			bakData[bakName].append((title,href,img,'',mode,1,'play',False,menu))
		if bakData.get(bakName):xrw('sysmenu.dat',json.dumps(bakData));mess('buff list ok',timeShown=100)
	
	elif query=="page":
		bakData[bakName]=page_detail(url)
		if bakData.get(bakName):xrw('sysmenu.dat',json.dumps(bakData));mess('buff list ok',timeShown=100)
	
	elif query=='play':
		epi=xsearch('T???p-(\d+) ',name)
		if not epi:epi='1'
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		items,sub=hdo.getLink(url,epi)
		link=gdl(items)
		if link:
			xbmcsetResolvedUrl(link)
			if sub:
				if 'hdonline.vn' in sub:
					if not sub.startswith('http'):sub='http://data.hdonline.vn/api/vsub.php?url=%s'%sub
					s=xread('http://data.hdonline.vn/api/vsub.php?url='+sub)
					subname=joinpath(subsfolder,os.path.basename(sub).split('?')[0]+'-Vie.sub')
					makerequest(subname,s,'wb')
				else:subname=sub
				xbmc.sleep(1000);xbmc.Player().setSubtitles(subname);mess(u'Sub c???a HDOnline.vn')
		else:mess('File invalid or deleted!','hdonline.vn') 

	elif query=='play':
		epi=xsearch('T???p-(\d+) ',name)
		if not epi:epi='1'
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		j=hdo.getLink(url,epi)
		link=''
		if j:
			L=sorted(j, key=lambda k: k[1],reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print href,L
			for href,r in L:
				link=dl(href)#;print 'a',link,'b',href
				if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','hdonline.vn') 

	elif query=='play':
		from resources.lib.servers import hdonline;hdo=hdonline(c)
		hdo.getLink(url)
		if 'http://hdonline.vn/frontend/episode/xmlplay' not in url:
			l=hdo.eps(url)
			if l:url=l[0][1]
		items,sub=hdo.maxLink(url+'&format=json&_x=%s'%str(random.random()))
		link=gdl(items);print items,sub
		if link:
			xbmcsetResolvedUrl(link)
			if sub:
				if 'hdonline.vn' in sub:
					if not sub.startswith('http'):sub='http://data.hdonline.vn/api/vsub.php?url=%s'%sub
					s=xread('http://data.hdonline.vn/api/vsub.php?url='+sub)
					subname=joinpath(subsfolder,os.path.basename(sub).split('?')[0]+'-Vie.sub')
					makerequest(subname,s,'wb')
				else:subname=sub
				xbmc.sleep(1000);xbmc.Player().setSubtitles(subname);mess(u'Sub c???a HDOnline.vn')
		else:mess('File invalid or deleted!','hdonline.vn') 

def kphim(name,url,img,mode,page,query):
	hd={'User-Agent':'Mozilla/5.0'};c='lightgreen'
	color['kphim']='[COLOR lightgreen]'
	ico=os.path.join(iconpath,'kphim.png');urlhome='http://kphim.tv/'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://kphim.tv/resources/images/logo.png').body,'wb')
		except:pass
		
	from resources.lib.servers import kPhim;kph=kPhim(c)
	if  query=='kphim.tv':
		a=xread(urlhome)
		title=color['search']+"Search tr??n kphim.tv[/COLOR]"
		addir_info(title,'kphim.tv',ico,'',mode,1,'search',True)
		
		for title in re.findall('<div class="title-tab">.*?\s(.+?)\s.*?</div>',a):
			addir_info(namecolor(title.strip(),c),urlhome,ico,'',mode,1,'new',True)
		
		b=xsearch('(<nav id="footer-nav">.+?</ul>)',a,1,re.S)
		for href,title in re.findall('<li><a href="(.+?)">(.+?)</a></li>',b):
			if 'theloai' in href:addir_info(namecolor(title,c),href,img,'',mode,1,'theloai',True)
			else:addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
			
		title='PHIM TRUY???N H??NH H??N QU???C'
		href='http://kphim.tv/theloai/phim-truyen-hinh-han-quoc-z1.html'
		addir_info('[COLOR lime]'+title+'[/COLOR]',href,img,'',mode,1,'theloai',True)
		l=re.findall('(<div class="kdrama-item.+?</div>)',a,re.S)
		for title,href,img in kph.detail(l):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
		
		title='TV SHOW, TRUY???N H??NH TH???C T???'
		href='http://kphim.tv/theloai/truyen-hinh-thuc-te-z2.html'
		addir_info('[COLOR lime]'+title+'[/COLOR]',href,img,'',mode,1,'theloai',True)
		l=re.findall('(<div class="kshow-item.+?</div>)',a,re.S)
		for title,href,img in kph.detail(l):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="kphim.tv":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return
		
		search_string = urllib.quote_plus(query)
		url='http://kphim.tv/search/?keyword=%s'%search_string
		for title,href,img in kph.genre(url):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
	
	elif query=='new':
		if 'TOP' in name:s=xsearch('(%s.+?<script>)'%namecolor(name),make_request(urlhome),1,re.DOTALL)
		else:s=xsearch('(%s.+?</ul>)'%namecolor(name),make_request(urlhome),1,re.DOTALL)
		for href,title,label in set(re.findall('href="(.+?)" title="(.+?)".+?> ([^>]+?)</span>',s)):
			addir_info(namecolor(title+' - '+label,c),href,img,'',mode,1,'episode',True)

	elif query=='theloai':
		for title,href,img in kph.genre(url):
			addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
	
	elif query=='episode':
		for href,title in kph.eps(url):
			addir_info('T???p %s - '%title+namecolor(name),href,img,'',mode,1,'play')
	
	else:
		link=kph.getLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','kphim.tv') 

def phimnhanh(name,url,img,mode,page,query):
	color['phimnhanh']='[COLOR chartreuse]'
	ico=os.path.join(iconpath,'phimnhanh.png');urlhome='http://phimnhanh.com/'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://cdn.phimnhanh.com/assets/images/logo.png').body,'wb')
		except:pass
	def namecolor(name,c='chartreuse'):return '[COLOR %s]'%c+name+'[/COLOR]'
	def nocolor(name):return re.sub('\[.+?\]','',name)
	def detail(body):
		hrefs=[]
		for  s in re.findall('(<li  class="serial">.+?</li>)',body,re.DOTALL):
			href=xsearch('href="(.+?)"',s)
			if href not in hrefs:hrefs.append(href)
			else:continue
			title=xsearch('title="(.+?)"',s)
			img=xsearch('data-original=="(.+?)"',s)
			label=xsearch('<span class="m-label q">(.+?)</span>',s)
			lang=xsearch('<span class="m-label lang">(.+?)</span>',s)
			ep=xsearch('<span class="m-label ep">(.+?)</span>',s)
			if lang:title=lang+' '+title
			if label:title=label+' '+title
			if ep:title+=' '+ep
			addir_info(namecolor(title),href,img,'',mode,1,'series',True)
		np=xsearch('<a href="([^>]+?)" rel="next">',body)
		if np:
			np=np.replace('amp;','');pn=xsearch('page=(\d+?)\Z',np)
			ps=xsearch('<a href="[^>]+?">(\d+?)</a></li> <li><a href="[^>]+?" rel="next">',body)
			t=color['trangtiep']+' Trang tiep theo...trang %s/%s[/COLOR]'%(pn,ps)
			addir_info(t,np,ico,'',mode,page+1,query,True)
	
	if query=='phimnhanh.com':
		title=color['search']+"Search tr??n phimnhanh.com[/COLOR]"
		addir_info(title,'phimnhanh.com',ico,'',mode,1,'search',True)

		body=get_home_page('phimnhanh.html',urlhome)
		s=xsearch('(<div id="menu-fixed".+?</ul>)',body,1,re.DOTALL)
		for h,t ,l in re.findall('href="(.+?)".+?<span class="h_">(.+?)</span>(.+?)</a>',s):
			addir_info(namecolor(t+l),h,ico,'',mode,1,'main',True)
		
		for title in re.findall('<li class=".*?" data-id=".*?">.*\s.*<p>(.+?)</p>',body):
			addir_info(namecolor(title),'',ico,'',mode,1,'submenu',True)
		
		add_sep_item('---------------HOT-------------------------------------------------')
		s=xsearch('(<ul id="slide-top">.+?</ul>)',body,1,re.DOTALL)
		for h,t,i  in re.findall('<a href="(.+?)" title="(.+?)".+?url\(\'(.+?)\'',s):
			addir_info(namecolor(t),h,i,i,mode,1,'series',True)
			
		s=xsearch('(<div class="more col">.+?<section class="cat-gr full">)',body,1,re.DOTALL)
		for h,t,i  in re.findall('<a href="(.+?)" title="(.+?)".+?src="(.+?)"',s):
			addir_info(namecolor(t),h,i,i,mode,1,'series',True)
		
		add_sep_item('---------------MORE-------------------------------------------------')
		detail(body)

		if get_home_page('phimnhanh.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return kphim(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phimnhanh.com":
		url='http://phimnhanh.com/danh-sach-phim/?s='+urllib.quote_plus(query)
		query='main'#xu ly pagenext
		detail(make_request(url))
	
	elif query=='submenu':
		body=get_home_page('phimnhanh.html',urlhome)
		s=xsearch('(<p>%s</p>.+?</ul>)'%nocolor(name).strip(),body,1,re.DOTALL)
		for h,t in re.findall('href="(.+?)" title="(.+?)"',s):
			addir_info(namecolor(t),h,ico,'',mode,1,'main',True)

	elif query=='main':detail(make_request(url))
			
	elif query=='series':
		body=make_request(url);s=xsearch('(<p class="epi">.+?    </p>)',body,1,re.DOTALL)
		for h,t in re.findall('href="(.+?)" title=".+?">(.+?)</a>',s):
			addir_info('T???p %s '%t+nocolor(name),h,img,'',mode,1,'play')
		
	else:
		a=make_request(url.replace('/phim/','/xem-phim/'))
		link=xsearch('playlist: "(.+?)"',a);a=make_request(link)
		for s in re.findall('(label="\d+p")',a):a=re.sub(s,'label="'+xsearch('label="(\d+)p"',s)+'"',a)
		a=a.replace('hd1080','1080').replace('hd720','720').replace('large','640').replace('medium','480')
		items=re.findall('file[^"]+"(.+?)"[^"]+"(\d+)"',a)
		if myaddon.getSetting('resolut')=='Max':items=sorted(items, key=lambda k: int(k[1]),reverse=True)
		else:items=sorted(items, key=lambda k: int(k[1]))
		if items:
			link=''
			for href,label in items:
				response=make_request(href.replace('amp;',''),resp='o')
				if response and response.status==302:
					href=response.headers.get('location')
					if make_request(href,resp='s')==200:link=href;break
				if not link:xbmc.sleep(1000)
			if link:xbmcsetResolvedUrl(link)
			else:mess('File invalid or deleted!','phimnhanh.com') 
		else:
			link=xsearch('file="(.+?)"',a).replace('amp;','')
			if link and '.youtube.com' in link:play_youtube(link)
			else:mess('File invalid or deleted!','phimnhanh.com') 

def htvonline(name,url,img,fanart,mode,page,query):
	tvurl='http://www.htvonline.com.vn/livetv';showurl='http://www.htvonline.com.vn/shows'
	phimurl='http://www.htvonline.com.vn/phim-viet-nam';hd['X-Requested-With']='XMLHttpRequest'
	def namecolor(name):return '[COLOR yellowgreen]%s[/COLOR]'%name
	if query=='home':
		tv=makerequest(joinpath(xsharefolder,'htvtv.html'));show=makerequest(joinpath(xsharefolder,'htvshow.html'))
		phim=makerequest(joinpath(xsharefolder,'htvphim.html'))
		for title in re.findall('<div class="view_title2"><div>(.+?)</div>',tv):
			addir(namecolor(title.replace(',','-')),tvurl,img,'',mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',show)
		addir(namecolor('TV Shows'),showurl+'?page=1',fanart,fanart,mode,page,'submenu',True)
		fanart=xsearch('<img width="487" height="274" src="(.+?)"',phim)
		addir(namecolor('Phim'),phimurl+'?page=1',fanart,fanart,mode,page,'submenu',True)
		for title,detail in re.findall('<div class="view_title"><div>(.+?)</div>(.+?)</ul>',show,re.DOTALL):
			#addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
			add_sep_item(title)
			for href,label,img in re.findall('data-tooltip=".+?".+?<a href="(.+?)".+?<h2>(.+?)</h2>.+? src="(.+?)"',detail,re.DOTALL):
				addir(label,href,img,'',mode,page,'htvplay')
		if checkupdate('htvtv.html',8,xsharefolder):
			endxbmc();makerequest(joinpath(xsharefolder,'htvtv.html'),make_request(tvurl),'w')
			makerequest(joinpath(xsharefolder,'htvshow.html'),make_request(showurl),'w')
			makerequest(joinpath(xsharefolder,'htvphim.html'),make_request(phimurl),'w')
	elif query=='submenu':
		if 'l???ch ph??t s??ng' in name:
			body=makerequest(joinpath(xsharefolder,'htvtv.html'))
			href='http://www.htvonline.com.vn/livetv/show-schedule';chanels=('HTV','VTV','VTC')
			items=re.findall('value="(.+?)" data-imagesrc="(.+?)">(.+?)</option>',body)
			for chanel,img,title in sorted([s for s in items if [i for i in chanels if i in s[2]]],key=lambda l:l[2]):
				addir(namecolor(title.replace(',','-')),href,img,'',mode,int(chanel),'schedule',True)
		elif showurl in url or phimurl in url:
			if showurl in url:page1='htvshow.html';page2='htvshowpage.html'
			else:page1='htvphim.html';page2='htvphimpage.html'
			if 'page=1' in url:body=makerequest(joinpath(xsharefolder,page1))
			else:body=makerequest(joinpath(xsharefolder,page2))
			if phimurl in url and 'page=1' in url:
				for title,detail in re.findall('<div class="view_title"><div>(.+?)</div>(.+?)</ul>',body,re.DOTALL):
					#addir('[COLOR lime]%s[/COLOR]'%title,'',img,'',mode,1,'no')
					add_sep_item(title)
					for href,label,img in re.findall('data-tooltip=".+?".+?<a href="(.+?)".+?<h2>(.+?)</h2>.+? src="(.+?)"',detail,re.DOTALL):
						addir(label,href,img,'',mode,page,'htvplay')
			for href,label,img in re.findall('href="(.+?)".*\s.*\s.*alt="(.+?)" src="(.+?)"',body):
				addir(namecolor(label),href,img,'',mode,1,'episode_show',True)
			href_next=xsearch('<a class="btn_channel_next page_hr" href="(.+?)"></a>',body)
			if href_next:
				page_next=xsearch('page=(\d{1,3})\Z',href_next)
				page_end=xsearch('\?page=(\d{1,3})"><span aria-hidden="true">',body)
				label='%sTrang ti???p theo: trang %s/%s[/COLOR]'%(color['trangtiep'],page_next,page_end)
				addir(label,href_next,img,'',mode,page,query,True)
				endxbmc();hd['X-Requested-With']='XMLHttpRequest';body=make_post(href_next,headers=hd,resp='b')
				makerequest(joinpath(datapath,page2),body,'w')
		else:
			body=makerequest(joinpath(datapath,'htvtv.html'))
			for title,detail in re.findall('<div class="view_title2"><div>(.+?)</div>.+?<ul class="listtv group small livetvDetail">(.+?)</ul>',body,re.DOTALL):
				if title.replace(',','-') in name:
					for hplus,href,img in re.findall('href="(.+?)" data-original="(.+?)">.+?src="(.+?)"></a>',detail):
						addir(xsearch('/([\w|-]+)-\d',hplus).upper(),href,img,'',mode,page,'htvplay')
	elif query=='episode_show':
		pattern='<a data-tooltip=.+?href="(.+?)".*?>([ |\d|\w|-]+?)</'
		label=re.sub('\[.+?\]','',name);items=re.findall(pattern,make_request(url),re.DOTALL)
		for href,adate in items:
			addir('%s %s'%(label,adate),href,img,'',mode,page,'htvplay')
		if not items:addir(label,url,img,'',mode,page,'htvplay')
	elif query=='htvplay':
		body=make_request(url);maxlink=xsearch('"(http:.+?\.m3u8\?.+?)"',body)
		if '/xem-show/' in url and not xsearch('\d{1,2}-\d{1,2}-\d{4}',name,0):
			pattern='<a data-tooltip=".+?".+?href="%s".*\s.*>(.+?)</span></a>'%url
			adate=xsearch(pattern,body)
			if adate:name='%s %s'%(re.sub('\[.+?\]','',name),adate)
		xbmcsetResolvedUrl(maxlink,'Maxlink%s'%name)
	elif query=='schedule':
		body=make_post(url,hd,{'date':datetime.date.today().strftime("%Y-%m-%d"),'id_live':'%d'%page},'j')
		try:body=body.get('html')
		except:body=''
		items=re.findall('<b>(.+?)</b>.+?title="(.+?)"',body,re.DOTALL);now=datetime.datetime.now().strftime('%H')
		for frame,title in [s for s in items if s[0].strip()>str(int(now)-1)]:
			addir('[COLOR green]%s[/COLOR] %s'%(frame,namecolor(title)),url,img,'',mode,page,'no')

def search_get_items(server='vaphim.com',mode=1):
	menu={'MySearch':{'action':'Add','server':['xshare.vn']}};srv=server.split('.')[0]
	items=[('%sNh???p chu???i t??m ki???m m???i tr??n[/COLOR] %s%s[/COLOR]'%(color['search'],color[srv],server),'getstringsearch')]
	if myaddon.getSetting('history')=='true':
		items+=[(s,'dosearch') for s in re.findall('<a>(.+?)</a>',makerequest(search_file))]
	for label,query in items:addir_info(label,'',icon[srv],'',mode,1,query,True,menu=menu)

def search_input_string(server='vaphim.com'):
	string=get_input('Nh???p chu???i (??t nh???t 3 k?? t???) t??n phim c???n t??m tr??n %s'%server);attr='a'
	if not string or len(string.strip())<3:return ''
	string=remove_tag(string)
	if not xsearch('<a>%s</a>'%string,makerequest(search_file)):
		makerequest(search_file,'<a>%s</a>\n'%string,'a');xbmc.executebuiltin("Container.Refresh")
	return string

def vaphim(name,url,img,fanart,mode,page,query):
	colo=xsearch('\[COLOR (.+?)\]',color['vaphim']);ico=icon['vaphim'];urlhome='http://vaphim.com/'
	hd['Cookie']=makerequest(joinpath(xsharefolder,'vaphim.cookie'))
	def home_page(fn,url='',update=False):
		fullfilename=joinpath(xsharefolder,fn);body=''
		if not update and os.path.isfile(fullfilename):body=makerequest(joinpath(xsharefolder,fn))
		elif not update and url:body=vp_readpage(url)
		elif update and url and checkupdate(fn,folder=xsharefolder):
			body=vp_readpage(url)
			if body:endxbmc();content=makerequest(fullfilename,body,'w')
		return body

	def vp_readpage(url):
		url=url.replace('https:','http:')
		cookie=urllib2.HTTPCookieProcessor();opener=urllib2.build_opener(cookie);urllib2.install_opener(opener)
		body=xread(url,hd)
		cookie=';'.join('%s=%s'%(i.name,i.value) for i in cookie.cookiejar)
		if cookie:makerequest(joinpath(xsharefolder,'vaphim.cookie'),cookie,'w')
		if not body:mess(u'Get vaphim data b??? l???i!','Vaphim.com')
		return body
	
	if query=='vaphim.com':
		body=home_page('vaphim.html',urlhome)
		label=color['search']+"Search tr??n vaphim.com[/COLOR]"
		addir_info(label,'vaphim.com',ico,'',mode,1,'search',True)
		addir_info(namecolor('Phim l???-Phim b???-Nh???c-VideoClip m???i nh???t-Xem nhi???u nh???t',colo),urlhome,ico,'',mode,1,'phimmoinhat',True)
		addir_info(namecolor('Danh M???c Ph??n Lo???i Phim',colo),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh M???c Phim Theo Th??? Lo???i - Qu???c Gia',colo),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh M???c Ph??n Lo???i Nh???c',colo),'',ico,'',mode,1,'mainmenu',True)
		addir_info(namecolor('Danh M???c C??c B??? S??u T???p',colo),'',ico,'',mode,1,'mainmenu',True)
		add_sep_item('Vaphim.com gi???i thi???u')
		pattern='<a class="featured-article" href="(.+?)".+?src="(.+?)[\?|\"].+?"bookmark">(.+?)</a>'
		for href,img,title in re.findall(pattern,body,re.DOTALL):
			addir_info(namecolor(remove_tag(title),colo),href,img,img,mode,1,'vp_getsubpage',True)
		if home_page('vaphim.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=='phimmoinhat':
		add_sep_item('Xem nhi???u nh???t');body=home_page('vaphim.html')
		for href,title in re.findall('<li><a href="(.+?)" title="(.+?)">',body):
			addir_info(namecolor(remove_tag(title),colo),href,ico,'',mode,1,'vp_getsubpage',True)
		pattern='<li class=.+?src="(.+?)[\?|\"].+?<a href="(.+?)".+? >(.+?)</a>'
		add_sep_item('Phim l??? m???i nh???t')
		for img,href,title in re.findall(pattern,xsearch('"index-featured2"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title),colo),href,img,'',mode,1,'vp_getsubpage',True)
		add_sep_item('Phim b??? m???i nh???t')
		for img,href,title in re.findall(pattern,xsearch('"index-featured3"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title),colo),href,img,'',mode,1,'vp_getsubpage',True)
		add_sep_item('Nh???c m???i nh???t')
		for img,href,title in re.findall(pattern,xsearch('"index-featured4"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title),colo),href,img,'',mode,1,'vp_getsubpage',True)
		add_sep_item('VideoClip m???i nh???t')
		pattern='<img.+?src="(.+?)[\?|\"].+?<a href="(.+?)".+?>(.+?)</a>'
		for img,href,title in re.findall(pattern,xsearch('"index-news"(.+?)</ul>',body,1,re.DOTALL),re.DOTALL):
			addir_info(namecolor(remove_tag(title),colo),href,img,'',mode,1,'vp_getclip',True)
	
	elif query=='mainmenu':
		body=home_page('vaphim.html')
		if name==namecolor('Danh M???c Ph??n Lo???i Phim',colo):
			pattern='<li><a href="/(category/phim-2/.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title,colo),urlhome+href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh M???c Phim Theo Th??? Lo???i - Qu???c Gia',colo):
			pattern='<li id=".+?" class="menu.+?"><a href="(.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title,colo),href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh M???c Ph??n Lo???i Nh???c',colo):
			pattern='<li><a href="/(category/music/.+?)">(.+?)</a></li>'
			for href,title in re.findall(pattern,body):
				addir_info(namecolor(title,colo),urlhome+href,ico,'',mode,1,'vp_getpage',True)
		elif name==namecolor('Danh M???c C??c B??? S??u T???p',colo):
			return vaphim(name,'http://vaphim.com/category/collection/',img,fanart,mode,page,'vp_getpage')
	
	elif query=='vp_getpage':
		href=url.split('?')[0] if page==1 else '%spage/%d/'%(url.split('?')[0],page)
		if len(url.split('?'))>1:href=href+'?'+url.split('?')[1]
		
		body=vp_readpage(href)#;print href
		if not body:return 'no'
		if re.search('<div class="search-home-title">Danh s??ch ????? xu???t</div>',body):
			mess(u'Xin l???i! kh??ng t??m th???y k???t qu??? d???a tr??n truy v???n c???a b???n.','Vaphim search',10000)
			add_sep_item('-----Kh??ng t??m th???y k???t qu???--->Danh s??ch ????? xu???t----')
		pattern='<a data=.+?src="(.+?)[\?|\"].+?<h3.+?><a href="(.+?)" rel=.+?>(.+?)</a></h3>'
		for img,href,title in re.findall(pattern,body,re.DOTALL):
			addir_info(namecolor(remove_tag(title),colo),href,img,'',mode,1,'vp_getsubpage',True)
		pagelast=xsearch("<span class='pages'>Trang \d{1,4} c???a (\d{1,4})</span>",body)
		if pagelast and int(pagelast)>page:
			name=re.sub('\[.+?\]','',name.split('-')[0].strip())
			name='%s%s - Trang ti???p theo: trang %d/%s[/COLOR]'%(color['trangtiep'],name,page+1,pagelast)
			addir_info(name,url,ico,'',mode,page+1,query,True)
	
	elif query=='vp_getclip':
		if 'youtube.com' in url:play_youtube(url)
		else:
			item=re.search("src='(.+?)'.+?src='([\w|:|/|\.]+youtube.com.+?)'",make_request(url,hd))
			if item:addir_info(remove_tag(name),item.group(2),item.group(1),'',mode,1,'vp_getclip')
			else:mess(u'Sorry! Kh??ng get ???????c n???i dung n??y tr??n vaphim.com','vaphim.com');return 'no'

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return vaphim(name,url,img,fanart,mode,page,query)
		else:return 'no'
	elif url=="vaphim.com":
		url='http://vaphim.com/?s='+urllib.quote_plus(query);query='vp_getpage'
		return vaphim(name,url,img,fanart,mode,1,'vp_getpage')
	
	elif query=='vp_getsubpage':
		body=vp_readpage(url);items=list();name=remove_tag(name.replace('Vaphim ',''))
		body=xsearch('<div id="post-(.+?)"fb-comments"',body,1,re.DOTALL)
		if not body:return 'no'
		if re.search('class=".+category-(game|phn-mm|ebooks).+"',body):
			mess(u'Sorry! Trang n??y kh??ng ph???i trang phim','Vaphim.com');return 'no'
		art=re.findall('<p><a href=".+?" rel="attachment.+?"><img src="(.+?)[\?|"]',body)
		if not art:art=['']
		tabs=re.findall('#(tabs-.+?)" >(.+?)<',body);i=0;j=len(art)-1
		if tabs:
			for tab,tab_label in tabs:
				content=xsearch('<div id="%s">(.+?)</div>'%tab,body,1,re.DOTALL)
				fanart=art[i];i=0 if i==j else (i+1)
				for href,fn in re.findall('<a href="(.+?)".*?>(.+?)</a>',content):
					fn='[COLOR green]%s[/COLOR] - %s'%(tab_label,remove_tag(fn))
					items.append((fn if fn else name,href,fanart))
		else:
			pattern='([\w|/|:|\.]+?fshare\.vn.+?|[\w|/|:|\.]+?subscene\.com.+?)[&|"|\'].+?>(.+?)</a>'
			for href,fn in re.findall(pattern,body):
				fn=remove_tag(fn);fanart=art[i];i=0 if i==j else (i+1);
				items.append((fn if fn else name,href,fanart))
		if items:
			add_sep_item('Links phim: '+name)
			for title,href,fanart in items:addir_info(title,href,img,fanart,mode,1)
		#------------------------------------------------------------------------------------------------
		trailer=xsearch('(http[\w|:|/|\.]+youtube.com.+?)[\"|\'|<|>| ]',body)
		if trailer:addir_info('[COLOR lime]Trailer[/COLOR] - '+name,trailer,img,fanart,mode,1,'vp_getclip')
		#------------------------------------------------------------------------------------------------
		items=re.findall('href="(.+?)".+?src="(.+?)[\?|"].+?alt=".+?".+?title="(.+?)"',body)
		if items:
			add_sep_item('Ch??? ????? t????ng t???')
			for href,img,title in items:
				title=namecolor('Vaphim - '+remove_tag(title),colo)
				addir_info(title,href,img,'',mode,1,'vp_getsubpage',True)
	return ''

def get_params():#print json.dumps(json["content"],indent=2,sort_keys=True)
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

def music(name,url,img,fanart,mode,page,query):
	title='[COLOR gold]chiasenhac.com[/COLOR]'
	addir_info(title,'http://chiasenhac.com/',os.path.join(iconpath,'chiasenhac.png'),'',45,1,'Home',True)
	
	title='[COLOR blue]nhaccuatui.com[/COLOR]'
	addir_info(title,'nhaccuatui.com',os.path.join(iconpath,'nhaccuatui.png'),'',46,1,'Home',True)
	
	title='[COLOR fuchsia]nhacdj.vn[/COLOR] (D??nh cho l?? tr??? - U40 kh??ng n??n v??o!)'
	addir_info(title,'nhacdj.vn',os.path.join(iconpath,'nhacdj.png'),'',42,1,'Home',True)
		
def nhacdj(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'nhacdj.png');urlhome='http://nhacdj.vn/';c='fuchsia'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('https://lh6.ggpht.com/gIx3RPsUEMcNbDA2hkM2OA6-MxONAJ9BtZBOwbCpOhU71pO601kxFWgdhkYfk7B2vA8=w300',ico)
		except:pass
	def detail(b):
		for s in re.findall('(class="song-name".+?</div>\s*</div>)',b,re.DOTALL):
			href=xsearch('href="([^"]+?)"',s)
			title=xsearch('title="([^"]+?)"',s)
			views=xsearch('class="song-listen">([^"]+?)</div>',s)
			if views:title+=' - [COLOR gold]%s[/COLOR]'%views
			upload=xsearch('title="[^"]+?">([^"]+?)</a>.?<i class="icon-caret-right">',s)
			if upload:title+=' - [COLOR blue]%s[/COLOR]'%upload
			addir_info(title,href,ico,'',mode,1,'play')
		
		p=xsearch('(<div class="pagination">.+?</div)',b,1,re.DOTALL).replace('\n','')
		if p:
			pn=xsearch('class="page active"[^"]+?href="([^"]+?)"',p)
			pages=xsearch('page=(\d+?)"[^<]+?>Cu???i</a>',p)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,pn,ico,'',mode,page+1,'djpage',True)

	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://nhacdj.vn/images/misc/logo-dj.png',ico)
		except:pass
	if query=='Home':
		body=get_home_page('nhacdj.html',urlhome)
		title=color['search']+"Search tr??n nhacdj.vn[/COLOR]"
		#addir_info(title,'nhacdj.vn',ico,'',mode,1,'search',True)
		
		s=xsearch('(<ul class="navbar">.+?</ul>)',body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)" title="(.+?)">',s):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'djpage',True)
		
		#add_sep_item('--------------PHIM M???I C???P NH???T-------------');page=1;tvhay_page(body)
		s=xsearch('(class="left-box-home".+?</div></div></div></div>)',body,1,re.DOTALL)
		label=xsearch('>([^<]+?)</h4>',s)
		if label:add_sep_item('%s'%label)
		for href,title in re.findall('href="(.+?)">(.+?)</a>',s):
			addir_info(title,href,ico,'',mode,1,'play')
		
		if get_home_page('nhacdj.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=='vdjpage':
		b=make_request(url)
		s=xsearch('(id="list-video-cat".+?class="[^<]+?">Cu???i</a>)',b,1,re.DOTALL)
		for href,title,img in re.findall('href="(.+?)" title="(.+?)"><img src="(.+?)"',s):
			addir_info(title,href,img,'',mode,1,'vplay')
		
		p=xsearch('(<div class="pagination">.+?>Cu???i</a>)',s,1,re.DOTALL).replace('\n','')
		if p:
			pn=xsearch('class="page active"[^"]+?href="([^"]+?)"',p)
			pages=xsearch('page=(\d+?)"[^<]+?>Cu???i</a>',p)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,pn,ico,'',mode,page+1,'vdjpage',True)
		
	elif query=='djpage':
		b=make_request(url)
		if url=='http://nhacdj.vn/Video-cat2.html': 
			s=xsearch('("child-cat-list".+?</ul>)',b,1,re.DOTALL)
			for href,title in re.findall('href="(.+?)">(.+?)</a>',s):
				addir_info(namecolor(title,c),href,ico,'',mode,1,'vdjpage',True)
			s=xsearch('(id="top-video-data".+?Xem th??m</a>)',b)#,1,re.DOTALL):
			for href,img,title in re.findall('href="([^<]+?)"><[^<]+?src="([^<]+?)"[^<]+?title="([^<]+?)"',s):
				addir_info(title,href,img,'',mode,1,'vplay')
		else:detail(b)
	
	elif query=='vplay':
		b=make_request(url)
		link=xsearch('(youtube.com/[^"]+?)&',b)
		if link:play_youtube('https://www.'+link)
		
	elif query=='play':# http://nhacdj.vn/category.xml http://nhacdj.vn/Nhac-San-Dam-Cuoi-alb828.xml http://nhacdj.vn/artist1.xml
		b=make_request(url);link=''
		link=xsearch('flashvars="file=(.+?)"',b);print link
		if link:link=dl(link)
		if link:xbmcsetResolvedUrl(link)
		else:
			link_=xsearch("file:.?'(.+?)'",b);print link
			if link_:link=dl(link_)
			if link:xbmcsetResolvedUrl(link)
			else:xbmcsetResolvedUrl(link_)#mess('File invalid or deleted!','nhacdj.vn') 

def nhaccuatui(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'nhaccuatui.png');urlhome='http://www.nhaccuatui.com/';c='turquoise'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKOJ_A9ybSZxzDgfG_cChKX84xkOjnCCkM36ptKxBNHxHOOCjc',ico)
		except:pass
		
	from resources.lib.servers import nhaccuatui;nct=nhaccuatui()
	if query=='Home':
		b=xread(urlhome);counter_pl=nct.getCounter_pl(b);counter_sg=nct.getCounter_sg(b)
		title=namecolor('Search tr??n nhaccuatui.com','lime')
		addir_info(title,'nhaccuatui.com',ico,'',mode,1,'search',True)
		for href,title in re.findall('<a rel="follow" href="([^"]+?)"[^<]+?>([^<]+?)</a>',b):
			if 'nghe-si' in href:q='nghe-si'
			elif 'su-kien' in href:q='su-kien'
			elif 'playlist-hero' in href:q='hero'
			else:q='menu'
			addir_info(namecolor(title,c),href,ico,'',mode,1,q,True)
		
		add_sep_item('-----Playlist m???i------')
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '"box-left-album"' in i]:
			title,href,img=nct.getDetail_pl(s,counter_pl)
			addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
	
		add_sep_item('-----B??i h??t m???i------')
		for s in [i for i in re.findall('(<li.+?/li>)',b,re.DOTALL) if '"box-content-music-list"' in i]:
			title,href,img=nct.getDetail_sg(s,counter_sg)
			addir_info(title,href,img,'',mode,1,'play')
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="nhaccuatui.com" or query=="INP" or query=="search-in":
		def make_list(i):
			tt,title,href,img=i
			if 'Page next:' in title:
				addir_info(title.replace('page',str(page+1)),href,img,'',mode,page+1,query,True)
			elif '/bai-hat/' in href:addir_info(title,href,img,'',mode,1,'play')
			elif '/playlist/' in href:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			elif '/video/' in href:addir_info(title,href,img,'',mode,1,'playvideo')
			elif '/nghe-si-' in href:
				title=namecolor('Ngh??? s?? '+title,c)
				addir_info(title,href.replace('.html','.bai-hat.html'),img,'',mode,1,'page',True)
			elif '/tim-kiem?q=' in href:
				title=namecolor('T??m ki???m theo c???m t??? [COLOR gold]%s[/COLOR]'%title,c)
				addir_info(title,href,img,'',mode,1,'search-in',True)
			elif tt=='1':addir_info(namecolor(title,'blue'),href,img,'',mode,1,'search-in',True)
		
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		
		items=nct.search(urllib.quote(query),url)
		
		j=[j for j in items if j[0]=='0']
		if j:
			add_sep_item('-----K???t qu??? t??m nhanh------')
			for i in j:make_list(i)
			add_sep_item('-----K???t qu??? ???????c ????? xu???t b???i NhacCuaTui------')
		for i in [j for j in items if j[0]!='0']:make_list(i)
	
	elif query=='menu':
		b=xread(urlhome)
		s=''.join([i for i in re.findall('(<a rel="follow".+?/ul>)',b,re.DOTALL) if  url in i]).replace('\\','')
		s=xsearch('(<ul.+?/ul>)',s)
		#f=open(r'd:\xoa1.html','w');f.write(s);f.close()
		for href,title in re.findall('href="([^"]+?)"[^<]+?>([^<]+?)</a>',s):
			if 'http' not in href:href='http://www.nhaccuatui.com'+href
			addir_info(namecolor(title,c),href,ico,'',mode,1,'BXH' if 'BXH' in name else 'page',True)
		
		if 'BXH' in name:
			for title,href,img in nct.getBXH(url):
				if not img:img=ico
				if 'COLOR lime' not in title:addir_info(title,href,img,'',mode,1,'play')
				else:addir_info(title,href,img,'',100,page+1,query)
	
	elif query=='hero':
		add_sep_item('-----PLAYLIST M???I THAM GIA TU???N N??Y------')
		for title,href,img in nct.getPage_hero(url):
			if 'Page next:' not in title:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			else:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
		
		href='http://www.nhaccuatui.com/playlist-hero-top-10.html'
		addir_info(namecolor('C??C CH??? ????? TR?????C','blue'),href,img,'',mode,1,'hero-10',True)
	
	elif query=='hero-10':
		for title,href,img in nct.getPage_hero_10(url):
			addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)

	elif query=='nghe-si':
		for title,href,img in nct.getNghesi(url):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
		
	elif query=='su-kien':
		for title,href,img,fanart in nct.getSukien(url):
			if not fanart:fanart=img
			addir_info(title,'http://event.nhaccuatui.com/'+os.path.basename(href),img,fanart,mode,1,'listSK',True)
		
	elif query=='listSK':
		for title,href,img in nct.listSukien(url):
			addir_info(title,href,img,fanart,mode,1,'playvideo')
	
	elif query=='BXH':
		for title,href,img in nct.getBXH(url):
			if not img:img=ico
			if 'COLOR lime' not in title:addir_info(title,href,img,'',mode,1,'play')
			else:addir_info(title,href,img,'',100,page+1,query)
		
	elif query=='page' and 'bai-hat' in url:
		if 'nghe-si' in url and page==1:
			title='[COLOR gold]Playlist[/COLOR] - '+name
			addir_info(title,url.replace('.bai-hat.html','.playlist.html'),ico,'',mode,1,'playlist',True)
			title='[COLOR gold]Video[/COLOR] - '+name
			addir_info(title,url.replace('.bai-hat.html','.mv.html'),ico,'',mode,1,'page',True)
			add_sep_item('-----B??i H??t %s ------'%namecolor(name))
		
		for title,href,img in nct.getPage_sg(url):
			if not img:img=ico
			if 'Page next:' not in title:addir_info(title,href,img,'',mode,1,'play')
			else:addir_info(title.replace('page',str(page+1)),href,img,'',mode,page+1,query,True)

	elif query=='page' and 'playlist' in url:
		for title,href,img in nct.getPage_pl(url):
			if 'Page next:' not in title:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			else:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
	
	elif query=='page'  and ('video-' in url or '.mv.' in url):
		for title,href,img in nct.getPage_video(url):
			if 'video' not in href and 'page' not in img:continue
			elif img=='link':addir_info(title,href,ico,'',mode,1,query,True)
			elif img=='page':addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
			else:addir_info(title,href,img,'',mode,1,'playvideo')
	
	elif query=='playlist' or 'chu-de' in url:
		for title,href,img in nct.getPlayList(url):
			if not title:continue
			elif '/playlist/' in href:addir_info(namecolor(title,c),href,img,'',mode,1,'playlist',True)
			elif img=='page':addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
			else:addir_info(title,href,img,'',mode,1,'playPL')
	
	elif query=='playPL':xbmcsetResolvedUrl(url)
	elif query=='play':xbmcsetResolvedUrl(nct.getLink(xsearch('\.(\w+)\.html',url)))	
	elif query=='playvideo':
		id=xsearch('\.(\w+)\.html',url)
		if not id:id=xsearch('src="http://www.nhaccuatui.com/vh/auto/(\w+)\?',xread(url))
		xbmcsetResolvedUrl(nct.getLink(id,'video'))

def chiasenhac(name,url,img,fanart,mode,page,query):
	hd={'User_Agent':'Mozilla/5.0 (Android 4.4; Mobile; rv:42.0) Gecko/41.0 Firefox/42.0'}
	if myaddon.getSetting('resolut')=='Max':hd['Cookie']='vq=i%3A1080%3B; mq=i%3A500%3B'
	else:hd['Cookie']='vq=i%3A720%3B; mq=i%3A500%3B'
	ico=os.path.join(iconpath,'chiasenhac.png');icodj=os.path.join(iconpath,'nhacdj.png');urlhome='http://chiasenhac.vn/'
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://chiasenhac.com/templates/light2012/images/logo.jpg',ico)
		except:pass
	menu={'MyPlaylist':{'action':'Add','server':['chiasenhac.com']}}
	url=url.replace('.com','.vn')
	def csn_url(url):return urlhome+url if 'http://' not in url else url
	
	def csn_get_dir(s,art=dict(),isFolder=False):
		result=re.search('<a href="(.+?)" title="(.+?) - (.+?)"',s)
		if not result:result=re.search('<a href="(.+?)".+?"_top">(.+?)</a>.*[\n|](.+?)[\n|].*</span>',s)
		if not result:result=re.search('<a href="(.+?)".+?>(.+?)</a><br />\s+?(\S.+?)\n',s)
		if result:
			href=csn_url(result.group(1))
			t1=result.group(2).strip();t2=result.group(3).strip()
			img=art.get(href,xsearch('<img src="(.+?)"',s,result=ico))
			res=xsearch('<span style=".+?">(.+?)</span>',s)
			p1='<p class="middle">([\d|\.]+?)</p>';p2='<span class="gen">([\d|\.]+?)</span><br />'
			d1=xsearch(p1,s,result=xsearch(p2,s))
			p1='<span>([\d|\.|\:]+?)</span>';p2='<p>([\d|\.|\:]+?)</p>'
			p3='<span class="gensmall">([\d|\.|\:]+?)<br />'
			d2=xsearch(p1,s,result=xsearch(p2,s,result=xsearch(p3,s)))
			title='[COLOR red]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR green]%s[/COLOR]'%(res,d2,d1)
			if isFolder:
				title='[COLOR green]%s[/COLOR] [COLOR yellowgreen]%s[/COLOR] %s'%(t1,t2,title)
				addir_info(title,href,img,'',mode,1,'get_album',True,menu=menu)
			else:
				title='%s [COLOR yellowgreen]%s[/COLOR] %s'%(t1,t2,title)
				addir_info(title,href,img,'',mode,1,'csn_play',menu=menu)

	def csn_get_album(body):
		img=xsearch('"image_src" href="(.+?)"',body,result=ico)
		for s in re.findall('(<tr id=.playlist.+?</tr>)',body,re.DOTALL):
			result=re.search('<a href="(.+?)" class="musictitle".*?>([^<>].+?)</.+?>([^<>]+?)</span>',s)
			if result:
				href=csn_url(result.group(1))
				t1=result.group(2).replace('amp;','');t2=result.group(3).replace('-','').replace('amp;','').strip()
				label='%s [COLOR yellowgreen]%s[/COLOR]'%(t1,t2)
				addir_info(label,href,img,'',mode,1,'csn_play',menu=menu)

	def csn_video_main_page(body):
		subbody=xsearch('(<div class="h-main3".+?<div class="t2">)',body,1,re.DOTALL)
		result=re.search('<a href=".+?">(.+?)</a>.+?href="(.+?)"',subbody,re.DOTALL)
		if result:
			title='[COLOR lime]Playlist %s (Full)[/COLOR]'%result.group(1)
			addir_info(title,csn_url(result.group(2)),ico,'',mode,1,'get_album',True)
			pattern='<div class="gensmall"(.+?)class="info"'
			for s in re.findall(pattern,subbody,re.DOTALL):csn_get_dir(s)
		bodys=re.findall('(<div class="h-main3".+?</ul></div>)',body[body.find('class="t2"'):],re.DOTALL)
		for subbody in bodys:
			result=xsearch('class="cattitle">(.+?)</p>',subbody)
			if result:#M???i chia s???, Download m???i nh???t
				npage=xsearch('class="active_page"><a .+?><a href="(.+?)"',subbody)
				if npage:
					title='[COLOR lime]Video Clip/%s: Xem th??m[/COLOR]'%result
					addir_info(title,csn_url(npage),ico,'',mode,1,'get_video_page',True)
				else:
					title='[COLOR gold]Video Clip/%s  -----------------[/COLOR]'%result
					addir_info(title,'',ico,'',mode)
				for s in re.findall('<div class="gensmall"(.+?)class="info"',subbody,re.DOTALL):
					csn_get_dir(s)

	def csn_mp3_main_page(body):
		subbody=xsearch('(<th class="catLeft".+?</table>)',body,1,re.DOTALL)
		label=xsearch('\](.+?)[\:|\[]',name).replace('BXH','').strip()
		if subbody:
			if 'B???ng x???p h???ng' in name:#Album m???i chia s???
				result=re.search('"absmiddle"> <a href="(.+?)">(.+?)</a>',subbody)
				title='[COLOR lime]%s/%s: Xem th??m...[/COLOR]'%(label,result.group(2))
				href=result.group(1)
				if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_album_page',True)
			else:
				result=re.search('"absmiddle"> (.+?)</span>.+?<a href="(.+?)">',subbody,re.DOTALL)
				if result:
					title='[COLOR lime]%s/%s: Xem th??m...[/COLOR]'%(label,result.group(1))
					href=result.group(2)
					if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_album_page',True)
			art=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
			for s in re.findall('(<td title.+?</span></td>)',subbody,re.DOTALL):csn_get_dir(s,art,True)
		for subbody in re.findall('(class="ht-c".+?class="t2")',body,re.DOTALL):
			result=xsearch('<p style="float.+?">([^<].+?)</a>',subbody)
			if result:#Vi???t Nam, US-UK, Playback
				title='[COLOR lime]%s - Playlist (Full)[/COLOR]'%result
				href=xsearch('<a href="(.+?)" class="xt">',subbody)
				if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_album',True)
				for s in re.findall('("li-3".+?href=.+?</span></p>)',subbody,re.DOTALL):csn_get_dir(s)
			else:#M???i chia s???, Download m???i nh???t
				result=xsearch('<p style="float.+?">([^<].+?)</p>',subbody)
				if result:
					title='[COLOR lime]%s/%s: Xem th??m...[/COLOR]'%(label,result)
					href=xsearch('<a href="(.+?)" class="xt">',subbody)
					if href:addir_info(title,csn_url(href),ico,'',mode,1,'get_mp3_page',True)
					for s in re.findall('("text2".+?</span></p>)',subbody,re.DOTALL):csn_get_dir(s)
	
	def csn_get_album_page(body):
		art=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
		for subbody in re.findall('(class="catLeft".+?class="xt">.+?</a>)',body,re.DOTALL):
			result=re.search('<a href="(.+?)">(.+?)</a></span></th>',subbody)
			if result:
				title='[COLOR lime]%s[/COLOR]'%result.group(2)
				addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'get_album_page',True)
			elif not result:
				label=xsearch('"absmiddle"> (.+?)</span></th>',subbody)
				result=re.search('<a href="(.+?)".+?class="xt">(.+?)</a>',subbody)
				if label and result:
					if 'Quay v???' not in result.group(2):
						title='[COLOR lime]%s: %s - %s[/COLOR]'%(xsearch('\](.+?)[\:|\[]',name),label,result.group(2))
						addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'get_album_page',True)
					else:
						title='[COLOR lime]%s: %s[/COLOR]'%(xsearch('\](.+?)[\:|\[]',name),label)
						addir_info(title,'',ico,'',mode,1,'')
			for s in re.findall('class="gen"(.+?)</span></td>',subbody,re.DOTALL):csn_get_dir(s,art,True)
	
	def csn_search(url,string):
		if '?' not in url:
			setting={'None':'T??n b??i h??t/Ca s??','artist':'Ca s??','composer':'S??ng t??c','album':'T??n Album','lyric':		'L???i b??i h??t'}
			search_set=myaddon.getSetting('csn_s')#&mode=lyric
			m=''.join(s for s in setting if  setting.get(s)==search_set and s!='None')
			url='http://search.chiasenhac.com/search.php?s=%s&mode=%s'%(urllib.quote_plus(string),m)
		else:m=xsearch('mode=(.+?)\W',url+'&')
		body=xread(url)
		
		if m=='album':
			csn_get_album_page(body)
			next=xsearch('<a href="(.+?)" class="xt">Xem th??m...</a>',body)
			if next:
				title='[COLOR lime]Search: Xem th??m...[/COLOR]'
				addir_info(title,next.replace('amp;',''),ico,'',mode,1,query,True)
		else:
			imgs=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
			for s in re.findall('(<tr.+?/tr>)',body,re.DOTALL):
				href=xsearch('href="(.+?)"',s);t1=xsearch('target=".+?">(.+?)</a>',s)
				if not href or not t1:continue
				t2=xsearch('<p>([^<]+?)</p>\s+</div>',s)
				d1=xsearch('<span class="gen">(.+?)<br />',s)
				d2=xsearch('style="color: .+?">(.+?)</span>',s)
				d3=xsearch('<td nowrap="nowrap" align="center">\s+<p>(.+?)<p>',s)
				title='%s [COLOR yellowgreen]%s[/COLOR] [COLOR red]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR green]%s[/COLOR]'%(t1,t2,d2,d1,d3)
				href=csn_url(href);img=imgs.get(href,ico)
				addir_info(title,href,img,'',mode,1,'csn_play',menu=menu)
				result=re.search('<p>(.*?)<a href="(.+?)" title="(.+?)">.+?alt="Listen Album"',s)
				if result:#Playlist item
					t1=result.group(3).replace('Nghe playlist:','Playlist:')
					title='[COLOR green]%s[/COLOR] [COLOR yellowgreen]%s[/COLOR]'%(t1,result.group(1))
					addir_info(title,csn_url(result.group(2)),img,'',mode,1,'get_album',True)
			
			subbody=xsearch('(<th colspan="3" height="25">.+?</table>)',body,1,re.DOTALL)
			result=xsearch('<th colspan="3" height="25">(.+?)</th>',subbody)
			if result:#Album result
				addir_info('[COLOR gold]-----%s-----[/COLOR]'%result,'',ico,'',mode,1,'No')
				for i in re.findall('<a href="(.+?)" title="(.+?)".+?</a>(.*?)<br />\s.*\s.*<span style.+?>(.+?)</span>',subbody):
					img=imgs.get(i[0],ico)
					title='[COLOR green]%s[/COLOR] [COLOR yellowgreen]%s[/COLOR] [COLOR red]%s[/COLOR]'%(i[1],i[2],i[3])
					addir_info(title,csn_url(i[0]),img,'',mode,1,'get_album',True)
		
			npage=re.search('class="active_page"><a .+?><a href="(.+?)" class="npage">(.+?)</a>',body)
			if npage:
				title='[COLOR lime]Search: [COLOR yellow]%s[/COLOR]- Trang %s[/COLOR]'%(string,npage.group(2))
				addir_info(title,csn_url(npage.group(1).replace('amp;','')),img,'',mode,1,string,True)
	
	if query!='search' and query!='INF' and 'csn_Search_' not in query:
		body=make_request(urlhome) if query=='Home' else make_request(url,headers=hd)
	
	if query=='search':make_mySearch('','chiasenhac.com','','',mode,'get')
	elif query=="INP":csn_search(url,make_mySearch('',url,'','','','Input'))
	
	elif 'csn_Search_' in query:
		query=query.replace('csn_Search_','')
		setting={'None':'T??n b??i h??t/Ca s??','artist':'Ca s??','composer':'S??ng t??c','album':'T??n Album','lyric':
		'L???i b??i h??t'};myaddon.setSetting('csn_s',setting.get(query));xbmc.executebuiltin("Container.Refresh")
	
	elif 'search.php' in url or url=='chiasenhac.vn':csn_search(url,query)
	
	elif query=='Home':
		menu={'MyPlaylist':{'action':'Search','server':['chiasenhac.com']}}
		title='[COLOR lime]CSN Search theo[/COLOR] - [COLOR gold]%s[/COLOR] - Ph??m Func t??m kh??c'
		title=title%myaddon.getSetting('csn_s')
		addir_info(title,'chiasenhac.com',ico,'',mode,1,'search',True,menu=menu)
		
		title='[COLOR lime]My playlist - T??n Album[/COLOR]'
		addir_info(title,'http://chiasenhac.com/mp3/favourite',ico,'',mode,1,'myplaylist_album',True)
		
		title='[COLOR lime]My playlist - T??n B??i h??t[/COLOR]'
		addir_info(title,'http://chiasenhac.com/mp3/favourite',ico,'',mode,1,'myplaylist_baihat',True)
		
		for i in re.findall('style="white-space.+href="(.*?)" title="(.+?)"',body):#Main menu
			href=csn_url(i[0])
			addir_info('[COLOR green]%s[/COLOR]'%i[1],href,ico,'',mode,1,'submenu',True)
			
		for i in re.findall('<div class="[v|h]t[3|-][1|c]">(.+?)<div class=".2">',body,re.DOTALL):#Detail hompage
			result=re.search('<a href="(.+?)" class="cattitle">(.+?)</a>',i)
			if result:#BXH Video Clip, BXH Nh???c Vi???t Nam, BXH Nh???c US-UK
				title='[COLOR lime]%s[/COLOR]'%result.group(2)
				addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'main_page',True)
			else:
				result=re.search('<a href="(.+?)">(.+?)</a></span></th>',i)
				if result:#Album m???i chia s???
					title='[COLOR lime]%s[/COLOR]'%result.group(2)
					addir_info(title,csn_url(result.group(1)),ico,'',mode,1,'get_album_page',True)
				else:
					result=xsearch('<a href="(.+?)"',i);title=xsearch('>(.+?)</p>',i)
					if result and title:#Download m???i nh???t, M???i chia s???
						addir_info('[COLOR lime]%s[/COLOR]'%title,csn_url(result),ico,'',mode,1,'get_mp3_page',True)
					else:continue
			
			if 'Album' in title:
				art=dict(re.findall('<a href="(.+?)"><img src="(.+?)"',body))
				items=re.findall('(<td title.+?</span></td>)',i,re.DOTALL)
				for subbody in items:csn_get_dir(subbody,art,True)
			else:
				if 'Video' in title:items=re.findall('<div class="gensmall"(.+?)class="info"',i,re.DOTALL)
				elif 'Download' in title or 'chia' in title:items=re.findall('class="text2"(.+?</span></p>)',i,re.DOTALL)
				elif 'C???m' in title:items=re.findall('class="info"(.+?)lass="tip"',i,re.DOTALL)
				else:items=re.findall('class="texte1x"(.+?</span></p>)',i,re.DOTALL)
				for subbody in items:csn_get_dir(subbody)
	
	elif query=='submenu':
		title=xsearch('\](.+?)\[',name)
		subbody=xsearch('title="%s"(.+?)</ul>'%title,body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)" title="(.+?)"',subbody):#sub menu
			if 'Playlist' in name:
				addir_info('[COLOR green]%s[/COLOR]'%title,csn_url(href),ico,'',mode,1,'get_album',True)
			else:addir_info('[COLOR green]%s[/COLOR]'%title,csn_url(href),ico,'',mode,1,'main_page',True)
				
		if 'Playlist' in name:csn_get_album(body)
		elif 'Video Clip' in name:csn_video_main_page(body)
		else:csn_mp3_main_page(body)

	elif query=='main_page':
		if 'Video' in name:csn_video_main_page(body)
		elif 'BXH' in name:
			body=make_request(url)
			for i in re.findall('(<a href=".+?" class="cattitle">(.+?)</a>)',body):
				add_sep_item(i[1])
				subbody=xsearch('%s(.+?)</table>'%i[0],body,1,re.DOTALL)
				for s in re.findall('(<tr.+?/tr>)',subbody,re.DOTALL):csn_get_dir(s)
		else:csn_mp3_main_page(body)
				
	elif query=='get_video_page':
		for s in re.findall('"gensmall"(.+?)"info"',body,re.DOTALL):csn_get_dir(s)
		npage=re.search('class="active_page"><a .+?><a href="(.+?)" class="npage">(.+?)</a>',body)
		if npage:
			title='[COLOR lime]%s: Trang ti???p theo - Trang %s[/COLOR]'%(xsearch('\](.+?):',name),npage.group(2))
			addir_info(title,csn_url(npage.group(1)),ico,'',mode,1,'get_video_page',True)
		
	elif query=='get_mp3_page':#Download m???i nh???t, M???i chia s???, C???m nh???n m???i
		for s in re.findall('<tr class="\d{,4}(.+?)</tr>',body,re.DOTALL):csn_get_dir(s)
		npage=re.search('class="active_page"><a .+?><a href="(.+?)" class="npage">(.+?)</a>',body)
		if npage:
			title='[COLOR lime]%s: Xem th??m - Trang %s[/COLOR]'%(xsearch('\](.+?)[\:|\[]',name),npage.group(2))
			addir_info(title,csn_url(npage.group(1)),ico,'',mode,1,'get_mp3_page',True)

	elif query=='get_album_page':csn_get_album_page(body)
	
	elif query=='get_album':csn_get_album(body)
	
	elif 'myplaylist' in query:
		menu={'MyPlaylist':{'action':'Remove','server':['chiasenhac.com']}}
		from resources.lib.servers import chiasenhac
		csn=chiasenhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'));
		body=csn.get_favourite();csn.logout()
		imgs=re.findall('<a href="(.+?)" title=".+?"><img src="(.+?)"',body)
		for s in re.findall('(<tr class.+?/tr>)',body,re.DOTALL):
			result=re.search('<span class="musictitle"><a href="(.+?)" class="musictitle">(.+?)</a>',s)
			if result:
				href=csn_url(result.group(1))
				d1=result.group(2)
				d2=xsearch('<br /> <span class="gen">(.+?)</span>',s)
				d3=xsearch('<span style="color.+?">(.+?)</span>',s)
				d4=xsearch('<div style="position.+?">(.+?)<br />',s)
				d5=xsearch('<span class="postdetails">(.+?)</span>',s)
				#img=imgs.get(href,ico)
				img=[i[1] for i in imgs if os.path.basename(href) in i[0]]
				img=img[0] if img else ico
				title='%s [COLOR yellowgreen]%s[/COLOR] [COLOR red]%s[/COLOR] [COLOR yellow]%s[/COLOR] [COLOR green]%s[/COLOR]'%(d1,d2,d3,d4,d5)
				if query=='myplaylist_baihat':addir_info(title,href,img,'',mode,1,'csn_play',menu=menu)
				else:
					title='[COLOR green]%s[/COLOR]'%title;href=href.replace('/favourite/','/nghe-album/')
					addir_info(title,href,ico,'',mode,1,'get_album',True,menu=menu)

	elif query=='playlist_Add':
		from resources.lib.servers import chiasenhac
		csn=chiasenhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'));csn.favourite(url);csn.logout()
	elif query=='playlist_Remove':
		from resources.lib.servers import chiasenhac
		csn=chiasenhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'))
		csn.favourite(url,'remove');csn.logout();xbmc.executebuiltin("Container.Refresh")
	elif query=='playlist_RemoveAll':
		if mess_yesno('xshare c???nh b??o','Delete all in My Playlist? (Tr??? b??i h??t cu???i c??ng - hehehe)'):
			from resources.lib.servers import chiasenhac
			csn=chiasenhac(myaddon.getSetting('csn_u'),myaddon.getSetting('csn_p'));body=csn.get_favourite()
			for href in re.findall('<span class="musictitle"><a href="(.+?)" class="musictitle">.+?</a>',body):
				csn.favourite(csn_url(href),'remove')
			csn.favourite(csn_url(href));csn.logout();xbmc.executebuiltin("Container.Refresh")
	
	elif query=='csn_play':
		href=xsearch('decodeURIComponent\("(.+stream.+?)"\)',body)
		if 'http://' not in href:href=urllib.unquote(href)
		if '/m4a/' in href and '.m4a.' in href:href=href.replace('/m4a/','/flac/').replace('.m4a.','.flac.')
		xbmcsetResolvedUrl(href,img=xsearch('rel="image_src" href="(.+?)"',body))

def myNAS(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'mynas.png');urlhome=myaddon.getSetting('my_nas_url')
	username=myaddon.getSetting('my_nas_up')
	if not username or not username.split('/')[0].strip():username=''
	else:hd['Cookie']=makerequest(joinpath(xsharefolder,'mynas.cookie'))
	if not os.path.isfile(ico):
		try:urllib.urlretrieve('http://www.buffalo-asia.com/uploads/product/1299/ws5200d589.png',ico)
		except:pass
	
	def nas_login():
		if not username:return ''
		elif '/' not in username:mess(u'H??y set username/password ????ng quy ?????c cho acc NAS !','My NAS');return ''
		try:url_login=make_request(urlhome,resp='o').headers.get('location')+'rpc/login'
		except:return ''
		response=make_post(url_login,data={'user':username.split('/')[0],'password':username.split('/')[1]})
		if not response or response.status>302:mess('Login to NAS fail !','My NAS');return ''
		cookie=response.cookiestring
		f=open(joinpath(xsharefolder,'mynas.cookie'),'w');f.write(cookie);f.close()
		return cookie
	
	def nas_items(url,cookie='',loop=True):
		if cookie:hd['Cookie']=cookie
		js=make_request(url,hd,resp='j')
		i=[s for s in js if s.get('name')!='.' and s.get('name')!='..' and s.get('name')!='/' and s.get('name')!='.webaxs']
		if not i and loop:i=nas_items(url,nas_login(),False)
		return i
	
	if query=='home':
		response=make_request(urlhome,resp='o')
		if not response or response.status!=302:return
		url=response.headers.get('location')+'rpc/ls/';query=''
	
	elif query=='nas_play':
		direct_link=url.replace('/ls/','/download/')
		if username:direct_link+='|Cookie='+makerequest(joinpath(xsharefolder,'mynas.cookie'))
		return xshare_resolve(direct_link,os.path.splitext(direct_link)[1][1:].lower())
	
	detail=nas_items(url+urllib.quote(query))
	for title,href,dir in  [(s.get('name'),s.get('path'),s.get('directory')) for s in detail]:
		href=u2s(href);title=u2s(title)
		if str(dir) in 'True-true':addir_info('[COLOR gold]'+title+'[/COLOR]',url,ico,'',mode,page,href,True)
		else:addir_info(title,url+urllib.quote(href),ico,'',mode,page,'nas_play')

def bilutv(name,url,img,mode,page,query):
	hd={'User-Agent':'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'}
	ico=os.path.join(iconpath,'bilutv.png');urlhome='http://bilutv.com/'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://bilutv.com/images/logo.png').body,'wb')
		except:pass
		
	def namecolor(name,c='hotpink'):return '[COLOR %s]'%c+name+'[/COLOR]'
	def nocolor(name):return re.sub('\[.+?\]','',name)

	def page_items(body,c='film-item'):
		for s in re.findall('(<li class="%s">.+?</li>)'%c,body,re.DOTALL):
			href=xsearch('href="/(.+?)"',s)
			img=xsearch('data-src="(.+?)"',s)
			if not img:img=xsearch('data-original="(.+?)"',s)
			title=xsearch('<p class="name">(.+?)</p>',s)+' - '
			title+='[COLOR green] '+xsearch('<p class="real-name">(.+?)</p>',s)+'[/COLOR]'
			quality=xsearch('<span class="label-quality">(.+?)</span>',s)
			label=xsearch('<label class="current-status">(.+?)</label>',s)
			if re.search('T???p \d+|\d+/|/\d+|\+',label):
				title=namecolor(title)+' (%s%s)'%('' if not quality else quality+' ',label);dir=True;query='folder'
			else:title=title+' (%s%s)'%('' if not quality else quality+' ',label);dir=False;query='play'
			if 'Thuy???t Minh' in label:title='[COLOR blue]TM[/COLOR] '+title
			addir_info(title,urlhome+href,img,'',mode,1,query,dir)
	
	def get_episodes(body):
		s=xsearch('(<ul class="list-episode">.+?/ul>)',body,1,re.DOTALL)
		title=' '.join(s for s in re.sub('\[.+?\]','',name).split())
		items=re.findall('href="(.+?)">(.+?)</a>',s)
		for href,tap in items:
			addir_info('T???p '+tap+' - '+title,href,img,'',mode,1,'play')
		return items
	
	if query=='bilutv.com':
		body=get_home_page('bilutv.html',urlhome)
		title=color['search']+"Search tr??n bilutv.com[/COLOR]"
		addir_info(title,'bilutv.com',ico,'',mode,1,'search',True)
		s=xsearch('(<a href="/the-loai.+?"main-content")',body,1,re.DOTALL);menu_fail=True
		for href,title in re.findall('<a href="/(.+?)" title="(.*?)">',s):
			if not title:title=xsearch('<a href="/%s".+?</i><span>(.+?)</span>'%href,s)
			if [i for i in ('hoat-hinh','xem-nhieu','chieu-rap') if i in href]:
				addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'page',True)
			else:addir_info(namecolor(title),href,ico,'',mode,1,'menu',True);menu_fail=False
		
		add_sep_item('--------------Top--------------')
		s=xsearch('(<ul id="top-slide">.+?</ul>)',body,1,re.DOTALL)
		for title,href,img in re.findall('<a title="(.+?)" href="/(.+?)".+?data-src="(.+?)"',s):
			addir_info(title,urlhome+href,img,'',mode,1,'folder',True)
		
		if menu_fail:#Delete file bilutv.html if content resquest not full
			try:os.remove(joinpath(xsharefolder,'bilutv.html'))
			except:temp='';pass
		add_sep_item('--------------Hot--------------');page_items(body)
			
		if get_home_page('bilutv.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return bilutv(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="bilutv.com":
		search_string = urllib.quote_plus(query)
		url='http://bilutv.com/tim-kiem.html?q=%s'%search_string
		return bilutv(name,url,img,mode,1,'page')

	elif query=='menu':
		body=get_home_page('bilutv.html',urlhome)
		s=xsearch('(<a href="/%s".+?/ul>)'%url,body,1,re.DOTALL)
		if 'phim-le' in url:
			addir_info(namecolor('Phim l??? - T???t c???'),'http://bilutv.com/danh-sach/phim-le.html',ico,'',mode,1,'page',True)
		elif 'phim-bo' in url:
			addir_info(namecolor('Phim b??? - T???t c???'),'http://bilutv.com/danh-sach/phim-bo.html',ico,'',mode,1,'page',True)
		elif 'quoc-gia' in url:
			addir_info(namecolor('T???t c??? qu???c gia'),'http://bilutv.com/quoc-gia',ico,'',mode,1,'page',True)
		for href,title in re.findall('<a title=".+?" href="/(.+?)">(.+?)</a>',s):
			addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'page',True)
				
	elif query=='page':
		body=make_request(url)
		page_items(body,'film-item ')
		
		pn=re.search('<a href="/[^<]+?" >(\d+)</a></li><li><a href="/([^<]+?)" class="navigation next" rel="next">',body)
		if pn:
			href=urlhome+pn.group(2);pages=pn.group(1)
			title=color['trangtiep']+'Trang ti???p theo: trang %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,href,ico,'',mode,page+1,'page',True)
		else:
			pn=re.search('<a href="[^<]+?" >(\d+)</a></li><li><a href="([^<]+?)" class="navigation next" rel="next">',body)
			if pn:
				href=url.split('?')[0]+pn.group(2);pages=pn.group(1)
				title=color['trangtiep']+'Trang ti???p theo: trang %d/%s[/COLOR]'%(page+1,pages)
				addir_info(title,href,ico,'',mode,page+1,'page',True)

	elif query=='episodes':body=make_request(url);get_episodes(body)

	elif query=='folder':
		fanart=''
		if '/xem-phim/' not in url:
			body=make_request(url)
			fanart=xsearch('<img alt=".*?" src="(.+?)"',body)
			url=xsearch('<a href="(.*?/xem-phim/.+?)">',body)
			if urlhome not in url:url='http://bilutv.com'+url
		body=make_request(url)
		s=xsearch('(<ul class="choose-server">.+?/ul>)',body,1,re.DOTALL)
		if s and re.search('class="list-episode"',body):
			for href,title in re.findall('<a href="/(.+?)".*>([^<]+?)</a>',s):
				addir_info(title+' '+namecolor(name),urlhome+href,img,fanart,mode,1,'episodes',True)
			current=xsearch('<div class="playing"></div>(.+?)</a>',body)
			add_sep_item('--------------List of server: %s--------------'%current)
			get_episodes(body)
		elif s:
			label=' '.join(s for s in re.sub('\[.+?\]','',name).split())
			for href,title in re.findall('<a href="/(.+?)".*>([^<]+?)</a>',s):
				addir_info(title+' '+label,urlhome+href,img,fanart,mode,1,'play')
		else:
			s=get_episodes(body)
			if not s:
				label=' '.join(s for s in re.sub('\[.+?\]','',name).split());i=1
				s=re.findall('"(.+www.youtube.com.+)"',body)
				for href in s:
					addir_info('Link %d '%i+label,href,img,fanart,mode,1,'play_yt');i+=1
				if not s:addir_info(label,url,img,fanart,mode,1,'play')

	elif query=='play_yt':play_youtube(url)
	elif query=='play':
		from resources.lib.servers import gibberishAES
		if '/xem-phim/' not in url:
			url=xsearch('<a class="btn-see btn btn-danger" href="/(.+?)"',make_request(url))
			if urlhome not in url:url=urlhome+url
		
		try:c=gibberishAES(make_request(url));link=''
		except:c=link=''
		
		for h in re.findall('"(/episode/getlinkbackup/.+?)"',c):
			j=make_request('http://bilutv.com'+h,resp='j')
			try:L=[(s.get('file'),resolu(s.get('label'))) for s in j]
			except:L=[]
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print L
			for href,label in L:
				link=dl(href)
				if link:break
			if link:break

		if not link:
			L=[]
			for s in re.findall('(\{file:decodeLink.+?\})',c):
				L.append((xsearch("\('(.+?)'",s),xsearch("\('.+?',(\d+)\)",s),resolu(xsearch("label:'(.+?)'",s))))
			L=sorted(L, key=lambda k: int(k[2]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print L
			if L:
				for href,id,label in L:
					try:href=gibberishAES(href, "bilutv.com454657883435677%s"%id)
					except:continue
					link=dl(href)
					if link:break
			
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','bilutv.com') 

def anime47(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'anime47.png');urlhome='http://anime47.com/'
	hd['Cookie']='location.href=1';gkplugins='http://dll.anime47.com/gkphp/plugins/gkpluginsphp.php'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://anime47.com/favicon.ico',headers=hd).body,'wb')
		except:pass
	
	def namecolor(name):return '[COLOR deepskyblue]'+name+'[/COLOR]'
	def get_item(s):
		href=urlhome+xsearch('href="./(.+?)"',s)
		img=xsearch('src="(.+?)"',s)
		title=xsearch('<p class="title2">(.+?)</p>',s)
		if not title:
			title=xsearch('title="(.+?)"',s).replace('...','').strip()
			temp=xsearch('>([^<]+?)</h3>',s).replace('...','').strip()
			if not title:title=temp
			elif temp and temp not in title:title=title+' - '+temp
		eps=xsearch('>(.{,3}/.{,3})</',s)
		if eps:title=title+' [COLOR blue]'+eps+'[/COLOR]'
		views=xsearch('"view">(.+?)</',s)
		if views:title=title+' [COLOR gold](views:'+views+')[/COLOR]'
		elif xsearch('>L?????t xem.+?>(\d+?)</',s):
			title=title+' [COLOR gold](views:'+xsearch('>L?????t xem.+?>(\d+?)</',s)+')[/COLOR]'
		addir_info(namecolor(title),href,img,'',mode,1,'episodes',True)
	
	if query=='anime47.com':
		body=get_home_page('anime47.html',urlhome)
		title=color['search']+"Search tr??n anime47.com[/COLOR]"
		addir_info(title,'anime47.com',ico,'',mode,1,'search',True)
		for i in ('Th??? lo???i','N??m S???n Xu???t','AnimeBD','Cartoon','Ongoing'):
			if i=='AnimeBD':href=urlhome+"the-loai/bluray-46/1.html";q='page'
			elif i=='Cartoon':href=urlhome+"the-loai/cartoon-34/1.html";q='page'
			elif i=='Ongoing':href=urlhome+"tag/ongoing.html";q='page'
			else:href='';q='menu'
			addir_info(namecolor(i),href,ico,'',mode,1,q,True)
			
		add_sep_item('-------Chi???u r???p--------')
		S=xsearch('("list_chieurap".+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):get_item(s)

		add_sep_item('-------XEM NHI???U TRONG NG??Y--------')
		S=xsearch('(XEM NHI???U TRONG NG??Y.+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):get_item(s)
		
		add_sep_item('-------Phim ????? C???--------')
		S=xsearch('(Phim ????? C???.+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):get_item(s)
			
		add_sep_item('-------M???i update--------')
		S=xsearch('(<div class="blockbody".+?<div id="right">)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):get_item(s)

		if get_home_page('anime47.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return anime47(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="anime47.com":
		search_string = urllib.quote_plus(query)
		url='http://anime47.com/search.php?q=%s'%search_string
		body=make_request(url,hd)
		for s in re.findall('(<li><a href.+?</li>)',body):
			href=urlhome+xsearch('href="/(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('<strong>([^<]+?)</strong>',s)
			temp=xsearch('<br>([^<]+?)<',s)
			if temp:title=title+' '+temp
			addir_info(namecolor(title),href,img,'',mode,1,'episodes',True)

	elif query=='menu':
		body=get_home_page('anime47.html',urlhome)
		if 'Th??? lo???i' in name:
			s=xsearch('(<div class="theloai_menu">.+?</ul>)',body,1,re.DOTALL)
			for title,href in re.findall('<a title="(.+?)" href="./(.+?)"',body):
				addir_info(namecolor(title),urlhome+href,ico,'',mode,1,'page',True)
		elif 'N??m S???n Xu???t' in name:
			for title,href in re.findall('<li><a title="(.+?)" href="(http://anime47.com/tim-kiem/\?year=.+?)"',body):
				addir_info(namecolor(title),href,ico,'',mode,1,'page',True)
	
	elif query=='page':
		body=make_request(url,hd)
		for s in re.findall('(<div class="items">.+?</li>)',body,re.DOTALL):get_item(s)

		pn=xsearch("currentpage[^<]+?><span>\d*?</span>&nbsp;<a class='pagelink' href=./([^<]+?) onClick",body)
		if pn:
			if 'tim-kiem//2.html?' in pn:pn=pn.replace('tim-kiem//2.html?','tim-kiem/2.html/2.html?')
			href=urlhome+pn
			pl=xsearch("href=./([^<]+?) onClick='[^<]+?'><b>&raquo;</b></a>&nbsp;</div>",body)
			if pl and xsearch('/(\d+).html\?',pl):pl='/'+xsearch('/(\d+).html\?',pl)
			elif pl:pl='/'+xsearch('/(\d+).html',pl)
			title=color['trangtiep']+'Trang ti???p theo: trang %d%s[/COLOR]'%(page+1,pl)
			addir_info(title,href,ico,'',mode,page+1,'page',True)

	elif query=='episodes':
		body=make_request(url,hd)
		href=xsearch('<a class="play_info" href="(.+?)"',body)
		if href:
			body=make_request(href,hd)
			S=xsearch('(<td><div id="servers".+?</div></div></td>)',body)
			for s in re.findall('(<tr>.+?</tr>)',S):
				items=re.findall('href="(.+?)"><b>(.+?)</b>',s)
				server=xsearch('<font.+?>([^<]+?)</font>',s).strip()
				if len(items)>1:
					if server:add_sep_item('-------Server %s--------'%server)
					for href,tap in items:addir_info('T???p %s - '%tap+re.sub('\[.+?\]','',name),href,img,'',mode,1,'play')
				elif len(items)==1 and server:addir_info('Server %s '%server+re.sub('\[.+?\]','',name),href,img,'',mode,1,'play')
				elif len(items)==1:addir_info(re.sub('\[.+?\]','',name),href,img,'',mode,1,'play')
			
	elif query=='play':
		b=make_request(url,hd)
		url=xsearch('link:"(.+?)"',b)
		link=''
		if url:
			j=make_post(gkplugins,hd,{'link':url.replace('&','%26')},'j')
			#print j
			l=j.get('link',list)
			if l and isinstance(l, unicode):link=l
			elif l and isinstance(l, list):
				try:L=[(s.get('link'),resolu(s.get('label'))) for s in l]
				except:L=[]
				L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
				for href,label in L:
					link=dl(href)
					if link:break
		if link:xbmcsetResolvedUrl(link)
		elif not link:mess(u'Xin l???i! Link b???n mu???n xem c?? th??? ???? b??? h???ng')

def phimmedia(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'phim.png');urlhome='http://www.phim.media/'
	if not os.path.isfile(ico):
		b=make_request('http://www.phim.media/templates/themes/phim/images/phimmedia-s.png')
		if b:makerequest(ico,b,'wb')
	def namecolor(name):return '[COLOR orange]'+name+'[/COLOR]'
	def detail(s):
		href=xsearch('href="(.+?)"',s)
		title=xsearch('<div class="name"><a[^<]+?>(.+?)</div>',s,1,re.DOTALL)
		title=' '.join(s for s in re.sub('<[^<]+?>','',title).split())
		name2=' '.join(s for s in xsearch('"name2">([^<]+?)</div>',s,1,re.DOTALL).split())
		if name2:title=title+' - '+name2
		img=xsearch('src="(.+?)"',s)
		name3=' '.join(s for s in xsearch('class="status">([^<]+?)</div>',s,1,re.DOTALL).split())
		if name3:title=title+' - [COLOR gold]%s[/COLOR]'%name3
		if re.search('\d/\d',name3):addir_info(namecolor(title),href,img,'',mode,1,'series',True)
		else:addir_info(title,href,img,'',mode,1,'play')
	
	if query=='phim.media':
		body=get_home_page('phimmedia.html',urlhome)
		title=color['search']+"Search tr??n phim.media[/COLOR]"
		addir_info(title,'phim.media',ico,'',mode,1,'search',True)
		
		addir_info(namecolor('Phim m???i'),'http://www.phim.media/phim-moi/',ico,'',mode,1,'page',True)
		for title in re.findall('href="">([^<]+?)<span class="caret"',body):
			addir_info(namecolor(title),'',ico,'',mode,1,'menu1',True)
			
		add_sep_item('----------Movie-hot----------')
		for s in re.findall('(<div class="item">.+?</span></a>)',body,re.DOTALL):detail(s)
		
		S=xsearch('(id="tab_done" class="data-tab">.+?</li>\s*</ul>\s*</div>\s*</div>)',body,1,re.DOTALL)
		for s in re.findall('(<span class="data-tab-wrap-title">.+?</ul>)',S,re.DOTALL):
			label=xsearch('<span class="data-tab-wrap-title">(.+?)</span>',s)
			add_sep_item('----------M???i Ho??n Th??nh %s----------'%label)
			for j in re.findall('(<li>.+?</li>)',s,re.DOTALL):
				href=xsearch('href="(.+?)"',j)
				title=xsearch('title="(.+?)"',j)
				addir_info(namecolor(title),href,ico,'',mode,1,'series',True)

		top={'id="topviewday"':'Ng??y','id="topviewweek"':'Tu???n','id="topviewmonth"':'Th??ng'}
		tops=('id="topviewday"','id="topviewweek"','id="topviewmonth"')
		for i in tops:
			add_sep_item('----------Top Phim Xem Nhi???u: %s----------'%top[i])
			s=xsearch('(%s.+?</ul>)'%i,body,1,re.DOTALL)
			for j in re.findall('(<li>.+?</li>)',s,re.DOTALL):
				href=xsearch('href="(.+?)"',j)
				title=re.sub('<[^"]+?>','',xsearch('>([^"]+?)</p>',j))
				name2=' '.join(s for s in xsearch('<p>([^"]+?)</p>',j).split())
				if name2:title=title+' - '+name2
				addir_info(namecolor(title),href,ico,'',mode,1,'series',True)
		
		
		if get_home_page('phimmedia.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		mess(u'C??c b???n h??y like fanpage: https://www.facebook.com/PhimMedia nh??')  
	
	elif query=="menu1":
		name=re.sub('\[.+?\]','',name)
		body=get_home_page('phimmedia.html',urlhome)
		s=xsearch('(href="">%s<span class="caret".+?</ul>)'%name,body,1,re.DOTALL)
		for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s):
			href=os.path.dirname(href)+'/'+urllib.quote(os.path.basename(href))
			addir_info(namecolor(title),href,ico,'',mode,1,'page',True)
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimmedia(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phim.media":
		search_string = urllib.quote_plus(query)
		url='http://www.phim.media/index.php?keyword=%s&do=phim&act=search'%search_string
		return phimmedia(name,url,img,mode,page,'page')
			
	elif query=='page':
		body=make_request(url)
		S=xsearch('(<ul class="list-film">.+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):detail(s)
		pn=xsearch('<a href="([^<]+?)" class="NextBtn">Next</a>',body)
		if pn:
			pl=xsearch('<a href="([^<]+?)" class="NextBtn">Last</a>',body)
			p01=xsearch('page-(\d+)',pn)
			p02=xsearch('page-(\d+)',pl)
			p02='/'+p02 if p02 else ''
			title=color['trangtiep']+'Page next: %s%s[/COLOR]'%(p01,p02)
			addir_info(title,pn,ico,'',mode,page+1,'page',True)
			
	elif query=='series':
		name=re.sub('\[.+?\]','',name)
		body=make_request(url+'tap-1.html');fanart=''
		if not body:
			body=make_request(url)
			fanart=xsearch('<img alt=[^<]+?src="(.+?)"',body)
			link=xsearch('class="btn-watch" href="(.+?)"',body)
			if not link:return
			body=make_request(link)
		items=re.findall('(<h4>Server.+?</ul>)',body,re.DOTALL)
		for s in items:
			if len(items)>1:add_sep_item('---------- %s ----------'%xsearch('<h4>(.+?)</h4>',s))
			for href,title in re.findall('href="(.+?)" title="(.+?)"',s):
				addir_info(title+' '+name,href,img,fanart,mode,1,'play')
	
	elif query=='play':
		if url.endswith('.html'):body=make_request(url)
		else:
			href=url+'xem-online.html'
			body=make_request(href)
			if not body:
				body=make_request(url)
				link=xsearch('class="btn-watch" href="(.+?)"',body)
				if not link:return
				body=make_request(link)
		items=re.findall('<source src="(.+?)" type=.+? data-res="(.+?)"/>',body)
		link=''#;print items
		if myaddon.getSetting('resolut')=='Max':items=sorted(items, key=lambda k: k[1])
		else:items=sorted(items, key=lambda k: k[1],reverse=True)
		for href,label in items:
			link=dl(href)
			if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phim.media') 

def phimbathu(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'phimbathu.png');urlhome='http://phimbathu.com/';c='lightgray'
	if not os.path.isfile(ico):
		href='https://docs.google.com/uc?id=0B5y3DO2sHt1LeVZsMUQxbkUxWk0&export=download'
		response=make_request(href,resp='o',maxr=3)
		if  response.status==200:makerequest(ico,response.body,'wb')
	
	def detail(b):
		s=xsearch('(id="content".+?class="right-content")',b,1,re.DOTALL)
		for i in re.findall('(<li class="item.+?/li>)',s,re.DOTALL):
			title=xsearch('title="(.+?)"',i)
			label=xsearch('class="name-real">(.+?)</span>',i,1,re.DOTALL).replace('<span>','')
			label=' '.join(label.split())
			if label:title=title+' '+label
			label=xsearch('"label">(.+?)<',i)
			if label:title=title+' '+label
			if re.search('.huy???t .inh',i):title='[COLOR blue]TM[/COLOR] '+title
			href=xsearch('href="(.+?)"',i)
			if '//' not in href:href='http://phimbathu.com'+href
			img=xsearch('data-original="(.+?)"',i)
			addir_info(namecolor(title,c),href,img,'',mode,1,'episodes',True)
		pn=xsearch('<a href="([^<]+?)" class="navigation next"',s)
		if pn:
			pages=xsearch('>(\d+?)</a></li><li><a href="[^<]+?" class="navigation next"',s)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,'http://phimbathu.com'+pn,ico,'',mode,page+1,'page',True)

	
	if query=='phimbathu.com':
		b=get_home_page('phimbathu.html',urlhome)
		title=color['search']+"Search tr??n phimbathu.com[/COLOR]"
		addir_info(title,'phimbathu.com',ico,'',mode,1,'search',True)
		
		s='\n'.join(re.findall('(<li class="menu-item ">.+?</ul>)',b,re.DOTALL))
		for href,title in re.findall('href="([^"]+?)".+</i>(.+?)</a>',s):
			addir_info(namecolor(title,c),'http://phimbathu.com'+href,ico,'',mode,1,'menu',True)
			
		addir_info(namecolor('PHIM QUAN T??M',c),'http://phimbathu.com/film/AjaxView',ico,'',mode,1,'mostview',True)
		
		S=xsearch('<h2 class="title-box">(.+?End left-content)',b,1,re.DOTALL)
		for s in S.split('<h2 class="title-box">'):
			title=xsearch('>([^<]+?)</a>',s)
			add_sep_item('-------------%s--------------'%title)
			for i in re.findall('(<li.+?/li>)',s,re.DOTALL):
				title=xsearch('title="(.+?)"',i)
				label=xsearch('"label">(.+?)<',i)
				if label:title=title+' '+label
				if re.search('.huy???t .inh',i):title='[COLOR blue]TM[/COLOR] '+title
				href=xsearch('href="(.+?)"',i)
				if '//' not in href:href='http://phimbathu.com'+href
				img=xsearch('src="(.+?)"',i)
				addir_info(namecolor(title,c),href,img,'',mode,1,'episodes',True)
		
		if get_home_page('phimbathu.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")

	elif query=="menu":
		b=make_request(url)
		s=[i for i in re.findall('(<li class="menu-item ">.+?</ul>)',b,re.DOTALL) if xsearch('</i>(.+?)</a>',i) in name]
		if not s:return
		s=s[0]
		for href,title in re.findall('href="([^"]+?)">([^"]+?)</a>',s):
			addir_info(namecolor(title,c),'http://phimbathu.com'+href,ico,'',mode,1,'page',True)
			
		add_sep_item('--------------------------------------------');detail(b)

	elif query=="page":detail(make_request(url))
	elif query=="mostview":
		if url=='http://phimbathu.com/film/AjaxView':
			href=url+'?type=d'
			url='http://phimbathu.com/film/AjaxView?type=w'
			addir_info(namecolor('PHIM QUAN T??M TRONG TU???N',c),url,ico,'',mode,1,'mostview',True)
			url='http://phimbathu.com/film/AjaxView?type=m'
			addir_info(namecolor('PHIM QUAN T??M TRONG TH??NG',c),url,ico,'',mode,1,'mostview',True)
			add_sep_item('-------------PHIM QUAN T??M TRONG NG??Y-------------')
		else:href=url
		for i in re.findall('(<li.+?/li>)',make_request(href),re.DOTALL):
			title=xsearch('<span>(.+?)<',i)
			label=xsearch('"count_view">(.+?)<',i)
			if label:title=title+' [COLOR gold]%s[/COLOR]'%label
			if re.search('.huy???t .inh',i):title='[COLOR blue]TM[/COLOR] '+title
			href=xsearch('href="(.+?)"',i)
			if '//' not in href:href='http://phimbathu.com'+href
			addir_info(namecolor(title,c),href,ico,'',mode,1,'episodes',True)
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phimbathu(name,url,img,fanart,mode,page,query)
		else:return 'no'
	elif url=="phimbathu.com":
		search_string = urllib.quote_plus(query)
		return detail(make_request('http://phimbathu.com/tim-kiem.html?q='+search_string))

	elif query=='episodes':
		id=xsearch('(\d+).html',url);href='http://phimbathu.com/get-link-download-epi?id='+id
		b=make_request(href)#;print href,b
		items=re.findall('<a href="(.+?)">Download (.+?)</a>',b)#;print items
		for s in re.findall('<th>(.+?)</th>',b):
			ss=[i for i in items if xsearch('_(\w+).html',i[0]) in s]
			if ss:add_sep_item('-------------%s-------------'%s)
			for href,title in ss:
				if '//' not in href:href='http://phimbathu.com'+href
				title=title+' '+namecolor(name.replace('[COLOR blue]TM[/COLOR] ',''))
				addir_info(title,href,img,'',mode,1,'play')
	
	elif query=='play':
		s=re.findall('(<li data-link=.+?/li>)',make_request(url),re.DOTALL)
		L=[(xsearch('data-link="(.+?)"',i),resolu(xsearch('Download.* (\w+)',i))) for i in s]
		L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
		#print href,L
		if L:
			for href,r in L:
				link=dl(href)
				if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phimbathu.com') 
		
	elif query=='playAES':
		from resources.lib.servers import gibberishAES
		def link_default(s):
			a=xsearch('url[^"]+decodeLink\(([^(]+?)\)',s).replace('"','').replace("'",'')
			b=a.split(',');link=id=href=''
			if len(b)==2:
				s=b[0].strip();id=b[1].strip()
				try:href=gibberishAES(s, "phimbathu.com4590481877"+id)
				except:href=''
				if '://' not in href:href='http://phimbathu.com'+href
			else:return '',''
			hd['X-Requested-With']='XMLHttpRequest'
			L=make_request(href,hd,resp='j')
			L=[(i.get('file'),resolu(i.get('label'))) for i in L]
			L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			#print href,L
			if L:
				for href,r in L:
					link=dl(href)
					if link:break
			return link,id
		
		def link_bakup(s,id):
			link=id=''
			for s in re.findall('data-link="(.+?)"',b):
				#print s
				try:href=gibberishAES(s, "phimbathu.com4590481877"+id)
				except:href=''
				if not href:continue
				if '://' not in href:href='http://phimbathu.com'+href
				hd['X-Requested-With']='XMLHttpRequest'
				L=make_request(href,hd,resp='j')
				L=[(i.get('file'),resolu(i.get('label'))) for i in L]
				L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
				#print href,L
				if L:
					for href,r in L:
						link=dl(href)
						if link:break
			return link,id
		
		def link_all(s):
			s=re.findall('(\{[^\{]*decodeLink[^\{]*\})',c,re.DOTALL);link=id=''
			if not s:return '',''
			L=[(xsearch("decodeLink\('(.+?)'",i),xsearch("(\d+)\)",i),resolu(xsearch("label:.?'(.+?)'",i))) for i in s]
			L=sorted(L, key=lambda k: int(k[2]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
			if L:
				for s,id,r in L:
					try:href=gibberishAES(s, "phimbathu.com4590481877"+id)
					except:continue
					link=dl(href)
					if link:break
			return link,id

		b=make_request(url)
		link,id=link_all(b)
		if not link:link,id=link_default(b)
		if not link:link,id=link_bakup(b,id)
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','phimbathu.com') 

def phim14(name,url,img,mode,page,query):
	#http://www.dailymotion.com/video/k2Z6NnXtz8r2PUgJfMA 227414
	ico=os.path.join(iconpath,'phim14.png');urlhome='http://phim14.net/'
	#hd['Cookie']='location.href=1'
	if not os.path.isfile(ico):
		b=make_request('https://docs.google.com/uc?id=0B5y3DO2sHt1LZnkyYXQ4ckZaeDA&export=download',resp='o')
		if b.status==302:
			b=make_request(b.headers.get('location'),resp='o')
			if b.status==200:makerequest(ico,b.body,'wb')
	
	def namecolor(name):return '[COLOR chartreuse]'+name+'[/COLOR]'
	def make_item(s):
		href=xsearch('href="(.+?)"',s)
		title=xsearch('title="(.+?)"',s)
		if not title:title=xsearch('"title">(.+?)</div>',s)
		title=' '.join(s for s in title.split())
		title2=xsearch('<span class="status_r">(.+?)</span>',s)
		if not title2:title2=re.sub('&nbsp;|\[|\]','',xsearch('</a>([^<]+?)<',s))
		d=' '.join(s for s in title2.split())
		if d:title=title+' [COLOR green]('+d+')[/COLOR]'
		if 'TM' in d or 'Thuy???t Minh' in d:title='[COLOR gold]TM[/COLOR] '+title
		#if 'T???p' in d or 'Full' in d:q='episodes';dir=True;title=namecolor(title)
		#else:dir=False;q='play'
		img=xsearch('src="(.+?)"',s)
		if not img:img=ico
		addir_info(namecolor(title),href,img,'',mode,1,'episodes',True)
	
	def make_page_control(s):
		pn=xsearch('<a href="([^<]+?)">&raquo;</a></span>',s)
		if pn:
			p=xsearch('<span class="current">([^<]+?)</span>',s)
			p=re.sub('Page \d+? of','Page %s of'%(page+1),p)
			title=color['trangtiep']+'Page next: %s[/COLOR]'%p
			addir_info(title,pn,ico,'',mode,page+1,'page',True)
		
	if query=='phim14.net':
		body=get_home_page('phim14.html',urlhome)
		title=color['search']+"Search tr??n phim14.net[/COLOR]"
		addir_info(title,'phim14.net',ico,'',mode,1,'search',True)
		
		m=[('Th??? lo???i',''),('Qu???c Gia',''),('Phim L???',''),
			('Phim B???','http://phim14.net/danh-sach/phim-bo.html'),
			('Phim Chi???u R???p','http://phim14.net/danh-sach/phim-chieu-rap.html')]
		for i in m:
			addir_info(namecolor(i[0]),i[1],ico,'',mode,1,'page' if i[1] else 'menu',True)
			
		add_sep_item('-------Phim ??ang C???p Nh???t--------')
		S=xsearch('(class="blockbody blockrow link_film list_01" rel="dang-cap-nhat">.+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):make_item(s.replace('\n',''))
			
		add_sep_item('-------Phim ???? Ho??n Th??nh--------')
		S=xsearch('(class="blockbody blockrow link_film list_01" rel="da-hoan-thanh".+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):make_item(s.replace('\n',''))
		
		add_sep_item('-------Phim HOT--------')
		S=xsearch('(<div class="block" id="phimchieurap">.+?</ul>)',body,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):make_item(s)
		
		if get_home_page('phim14.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")

	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return phim14(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="phim14.net":
		search_string = urllib.quote_plus(query)
		url='http://phim14.net/search/%s.html'%search_string
		return phim14(name,url,img,mode,page,'page')
		body=make_request(url,hd)
		for s in re.findall('(<li><a href.+?</li>)',body):
			href=urlhome+xsearch('href="/(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('<strong>([^<]+?)</strong>',s)
			temp=xsearch('<br>([^<]+?)<',s)
			if temp:title=title+' '+temp
			addir_info(namecolor(title),href,img,'',mode,1,'episodes',True)

	elif query=='menu':
		if 'Phim L???' in name:
			body=make_request('http://phim14.net/danh-sach/phim-le.html')
			s=xsearch('(<li class="child"><a href="[^<]+?">Phim L???</a>.+?</ul>)',body,1,re.DOTALL)
			for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s):
				addir_info(namecolor(title),href,ico,'',mode,1,'page',True)
			S=xsearch('(<div id="content" class="container">.+?</a></span></div>)',body,1,re.DOTALL)
			for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):make_item(s)
			make_page_control(S)
		else:	
			body=get_home_page('phim14.html',urlhome)
			if 'Th??? lo???i' in name:
				s=xsearch('(<li class="child"><a>Th??? lo???i</a>.+?</ul>)',body,1,re.DOTALL)
				for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s):
					addir_info(namecolor(title),href,ico,'',mode,1,'page',True)
			elif 'Qu???c Gia' in name:
				s=xsearch('(<li class="child"><a>Qu???c gia</a>.+?</ul>)',body,1,re.DOTALL)
				for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s):
					addir_info(namecolor(title),href,ico,'',mode,1,'page',True)
		
	elif query=='episodes':
		href=xsearch('<a class="watch_button now" href="(.+?)"',make_request(url,hd))
		b=make_request(href,hd)
		S=re.findall('(<li class="server_item">.+?</ul>)',b,re.DOTALL)
		if len(S) == 0:
			s=xsearch('(<ul class="episode_list">.+?</ul>)',b,1,re.DOTALL)
			for href,title in re.findall('href="([^<]+?)"[^<]+?title="([^<]+?)"',s):
				addir_info(title,href,img,'',mode,1,'play')
		elif len(S)==1:
			for href,title in re.findall('href="([^<]+?)"[^<]+?title="([^<]+?)"',S[0]):
				addir_info(title,href,img,'',mode,1,'play')
		elif 'T???p' in name or re.search('/\d',name) or re.search('\d/',name):
			items=[];sep=[]
			for s in S:
				i=re.findall('href="([^<]+?)"[^<]+?title="([^<]+?)"',s)
				server=re.search('<img src="(.+?)"/>(.+?)</strong>',s)
				if server:
					if 'Daily' in server.group(2):continue
					c='VN' if 'vn.png' in server.group(1) else 'US'
					title=namecolor('[COLOR gold] Server %s (%s)[/COLOR] '%(server.group(2),c))+name.replace('[COLOR gold]TM[/COLOR] ','')
					addir_info(title,i[0][0],ico,'',mode,1,'server',True)
				if re.search('<li class="active">',s):sep=[server.group(2),c];items=i
			if items:
				add_sep_item('-------List of Server %s (%s)--------'%(sep[0],sep[1]))
				for href,title in items:
					addir_info(title,href,img,'',mode,1,'play')
		else:
			for s in S:
				server=re.search('<img src="(.+?)"/>(.+?)</strong>',s)
				if server:
					c='VN' if 'vn.png' in server.group(1) else 'US'
					add_sep_item('-------List of Server %s (%s)--------'%(server.group(2),c))
				for href,title in re.findall('href="([^<]+?)"[^<]+?title="([^<]+?)"',s):
					addir_info(title,href,img,'',mode,1,'play')
			
	elif query=='page':
		b=make_request(url,hd)
		S=xsearch('(<div id="content" class="container">.+?</span></div>)',b,1,re.DOTALL)
		for s in re.findall('(<li>.+?</li>)',S,re.DOTALL):make_item(s)
		make_page_control(S)

	elif query=='server':
		b=make_request(url,hd)
		S=[s for s in re.findall('(<li class="server_item">.+?</ul>)',b,re.DOTALL) if url in s]
		if S:
			ys=True if 'Youtube' in xsearch('(<strong><img src=.+?</strong>)',S[0]) else False
			for href,title in re.findall('href="([^<]+?)"[^<]+?title="([^<]+?)"',S[0]):
				if ys:href=href.replace('phim14.net','m.phim14.net')
				addir_info(title,href,img,'',mode,1,'play')
			
	
	elif query=='play':#http://player8.phim14.net/3008/plugins/plugins_player.php
		if 'm.phim14.net' in url:
			b=xsearch('(<div class="jp-player-video">.+?</div)',make_request(url),1,re.DOTALL)
			u=xsearch('src="(.+?)\?',b)
			if u:return play_youtube(u)
		b=xread(url)
		url=xsearch('link:"(.+?)"',b);print url
		link=''
		if url:
			href='http://player8.phim14.net/gkphp97pc/plugins/gkpluginsphp.php'
			b=xread(href,data='link='+url.replace('&','%26'))
			try:j=json.loads(b)
			except:j=[]
			#print 'j=%s'%j
			#makerequest(r'D:\xoa.js',json.dumps(j,indent=2),'a')
			def hh(l):
				L=[];link=''
				for i in l:
					j=i.get('link',[])
					L+=((s.get('link'),resolu(s.get('label'))) for s in j if s.get('label').lower()!='auto')
				L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
				for href,label in L:
					link=dl(href)
					if link:break
				return link
			
			l=j.get('list',list())
			if l:
				if isinstance(l, unicode):link=l
				elif l and isinstance(l, list):link=hh(l)
				elif l and (isinstance(l, dict) or isinstance(l, list)):#Kg sd
					for s in re.findall('(label="\d+p")',a):a=re.sub(s,'label="'+xsearch('label="(\d+)p"',s)+'"',a)
					a=a.replace('hd1080','1080').replace('hd720','720').replace('large','640').replace('medium','480')
					
					def get_max_link(link):
						b=make_request(link,resp='o',maxr=5)
						if b and b.history:link=b.history[-1].headers.get('location')
						else:link=''
						return link
					for i in l:
						k=i.get('link',list())#;print i.get('title')
						if k and isinstance(k, unicode):link=get_max_link(k)
						elif k and (isinstance(k, dict) or isinstance(k, list)):
							r=0
							for m in k:
								if m.get('label')=='HD':link=m.get('link')
								elif m.get('label')=='SD' and not link:link=m.get('link')
								else:
									try:
										if int(m.get('label').replace('p',''))>r:r=int(m.get('label').replace('p',''));link=m.get('link')
									except:pass
							if link:link=get_max_link(link)
						if link:break
			else:
				l=j.get('link',list())#;print 'aaaaaaaaaa %s'%l
				if l and isinstance(l, unicode):link=l
				elif l and isinstance(l, list):link=hh([j])
				elif l and (isinstance(l, dict) or isinstance(l, list)):#Kg sd
					r=0
					for i in l:
						try:
							if i.get('label')=='HD':link=i.get('link')
							elif i.get('label')=='SD' and not link:link=i.get('link')
							elif int(i.get('label').replace('p',''))>r:r=int(i.get('label').replace('p',''));link=i.get('link')
						except:pass
					if link:
						b=make_request(link,resp='o',maxr=5)
						try:link=b.history[-1].headers.get('location')
						except:link=''
		else:print 'String Not found'
		if link:xbmcsetResolvedUrl(link)
		elif not link:mess('File invalid or deleted!','phim14.net') 

	elif query=='play1':#http://player8.phim14.net/3008/plugins/plugins_player.php
		if 'm.phim14.net' in url:
			b=xsearch('(<div class="jp-player-video">.+?</div)',make_request(url),1,re.DOTALL)
			u=xsearch('src="(.+?)\?',b)
			if u:return play_youtube(u)
		b=make_request('http://phim14.net/ajax/episode.html?episodeid=%s'%xsearch('\.(\d+?)\.html',url),hd)
		url=xsearch('link:"(.+?)"',b)
		link=''
		if url:
			href='http://player8.phim14.net/gkphp93pc/plugins/gkpluginsphp.php'
			j=make_post(href,data={'link':url.replace('&','%26')},resp='j')
			#print 'j=%s'%j
			#makerequest(r'D:\xoa.js',json.dumps(j,indent=2),'a')
			def hh(l):
				L=[];link=''
				for i in l:
					j=i.get('link',[])
					L+=((s.get('link'),resolu(s.get('label'))) for s in j if s.get('label').lower()!='auto')
				L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
				for href,label in L:
					link=dl(href)
					if link:break
				return link
			
			l=j.get('list',list())
			if l:
				if isinstance(l, unicode):link=l
				elif l and isinstance(l, list):link=hh(l)
				elif l and (isinstance(l, dict) or isinstance(l, list)):#Kg sd
					for s in re.findall('(label="\d+p")',a):a=re.sub(s,'label="'+xsearch('label="(\d+)p"',s)+'"',a)
					a=a.replace('hd1080','1080').replace('hd720','720').replace('large','640').replace('medium','480')
					
					def get_max_link(link):
						b=make_request(link,resp='o',maxr=5)
						if b and b.history:link=b.history[-1].headers.get('location')
						else:link=''
						return link
					for i in l:
						k=i.get('link',list())#;print i.get('title')
						if k and isinstance(k, unicode):link=get_max_link(k)
						elif k and (isinstance(k, dict) or isinstance(k, list)):
							r=0
							for m in k:
								if m.get('label')=='HD':link=m.get('link')
								elif m.get('label')=='SD' and not link:link=m.get('link')
								else:
									try:
										if int(m.get('label').replace('p',''))>r:r=int(m.get('label').replace('p',''));link=m.get('link')
									except:pass
							if link:link=get_max_link(link)
						if link:break
			else:
				l=j.get('link',list())#;print 'aaaaaaaaaa %s'%l
				if l and isinstance(l, unicode):link=l
				elif l and isinstance(l, list):link=hh([j])
				elif l and (isinstance(l, dict) or isinstance(l, list)):#Kg sd
					r=0
					for i in l:
						try:
							if i.get('label')=='HD':link=i.get('link')
							elif i.get('label')=='SD' and not link:link=i.get('link')
							elif int(i.get('label').replace('p',''))>r:r=int(i.get('label').replace('p',''));link=i.get('link')
						except:pass
					if link:
						b=make_request(link,resp='o',maxr=5)
						try:link=b.history[-1].headers.get('location')
						except:link=''
		else:print 'String Not found'
		if link:xbmcsetResolvedUrl(link)
		elif not link:mess('File invalid or deleted!','phim14.net') 

def hdsieunhanh(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'hdsieunhanh.png');urlhome='http://hdsieunhanh.com/';c='orangered'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://hdsieunhanh.com/assets/img/layout/logo.png',headers=hd).body,'wb')
		except:pass
	
	def menu(s):
		for href,title in re.findall('<a href="([^"]+?)">.?<span class="tnico[^"]+?"></span>([^<]+?)</a>',s):
			href='menu' if 'javascript' in href else urlhome+href;title=title.strip()
			addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
	
	def banner(s):
		add_sep_item('-----Banner-----')
		s=xsearch('(<div id="banner">.+?<a href="/phim-hot.html">)',s)
		for i in s.split('"titinfo"'):
			href=xsearch('href="([^"]+?)"',i)
			if not 'phim-' in href:continue
			title=xsearch('(<span class=.tt_bold.>.+?class="nivo-caption-des">)',i)
			title=' '.join(re.sub('<[^<]+?>','',title).split())
			img=xsearch('href="%s"><img[^<]+?src="(.+?)"'%href,s)
			if 'Th???i l?????ng' in title:dir=False;query='play'
			else:dir=True;query='eps';title=namecolor(title,c)
			addir_info(title,href,img,img,mode,page,query,dir)
	
	def home_detail(s):
		s=[i for i in s.split('<div class="group-title-bg">') if 'class="viewmore"' in i or 'class="action"' in i]
		for s in s:
			i=re.search('<a href="([^"]+?)">([^<]+?)</a>',s)
			if i:
				href=i.group(1)
				href='' if 'javascript' in href else urlhome+href if 'http' not in href else href
				addir_info(namecolor('%s (all)-----'%i.group(2),'lime'),href,ico,'',mode,1,'page',True)
			for s in re.findall('(<li.+?/li>)',xsearch('(<ul.+?/ul>)',s)):
				i=sn.item(s)
				if i:addir_info(i[0],i[1],i[2],'',mode,page,'eps' if i[3] else 'play',i[3])
	
	from resources.lib.servers import sieunhanh;sn=sieunhanh()
	if query=='hdsieunhanh.com':
		b=get_home_page('hdsieunhanh.html',urlhome)
		title=color['search']+"Search tr??n hdsieunhanh.com[/COLOR]"
		addir_info(title,'hdsieunhanh.com',ico,'',mode,1,'search',True)
		
		menu(b);banner(b);home_detail(b)
		
		if get_home_page('hdsieunhanh.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="hdsieunhanh.com" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		for title,href,img,dir in sn.search(query):addir_info(title,href,img,'',mode,1,'eps' if dir else 'play',dir)

	elif url=='menu':
		b=get_home_page('hdsieunhanh.html',urlhome)
		i=[('TH??? LO???I','the-loai'),('QU???C GIA','quoc-gia'),('N??M PH??T H??NH','nam-phat-hanh')]
		j=''.join(m[1] for m in i if m[0] in name)
		for href,title in re.findall('<a[^<]+?href="(/%s/[^"]+?)"[^<]*?>([^<]+?)</a>'%j,b):
			addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,'page',True)
		
	elif query=='page':
		for title,href,img,dir in sn.page(url):
			if img!='image':addir_info(title,href,img,'',mode,page,'eps' if dir else 'play',dir)
			else:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page,'page',True)
			
	elif query=='eps':
		i=[('T???p %s %s'%(j[1],namecolor(name)),j[0]) for j in sn.eps(url)]
		if not i:i=[(namecolor(name),url)]
		for title,href in i:addir_info(title,href,img,fanart,mode,page,'play')
		
	elif query=='play':
		link=''
		for href,label in sn.maxLink(url):
			link=dl(href)#;print href,label
			if link:break
	
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','hdsieunhanh.com') 

def tvhay(name,url,img,mode,page,query):
	ico=os.path.join(iconpath,'tvhay.png');urlhome='http://tvhay.org/';c='gold'
	if not os.path.isfile(ico):
		href='https://docs.google.com/uc?id=0B5y3DO2sHt1LcmxSUm8yZ0dram8&export=download'
		response=make_request(href,resp='o',maxr=3)
		if  response.status==200:makerequest(ico,response.body,'wb')
	
	def detail(s):
		href=xsearch('href="(.+?)"',s)
		img=xsearch('data-original="(.+?)"',s)
		title=' '.join(re.sub('.em .him','',xsearch('title="(.+?)"><span',s)).split())
		lang=' '.join(i for i in xsearch('<div class="status">([^<]+?)</div>',s,1,re.DOTALL).split())
		if lang:title+=' - [COLOR blue]%s[/COLOR]'%lang
		year=' '.join(i for i in xsearch('<div class="year">([^<]+?)</div>',s,1,re.DOTALL).split())
		if year:title+=' - [COLOR green](%s)[/COLOR]'%year
		liked=' '.join(i for i in xsearch('<div class="liked">([^<]+?)</div>',s,1,re.DOTALL).split())
		if liked:title+=' [COLOR yellow]liked:(%s)[/COLOR]'%liked
		if re.search('.huy???t .inh',title):title='[COLOR green]TM [/COLOR]- '+title
		elif re.search('.???ng .i???ng',title):title='[COLOR blue]LT [/COLOR]- '+title
		elif re.search(' Sub ',title):title='[COLOR blue]Sub [/COLOR]- '+title
		if not re.search('\d+/\d+',title):addir_info(title,href,img,'',mode,1,'play')
		else:addir_info(namecolor(title,c),href,img,'',mode,1,'episode',True)
	
	def tvhay_page(u):
		b=make_request(u) if len(u)<200 else u
		for s in re.findall('(<div class="inner">.+?</li>)',b,re.DOTALL):detail(s)
		
		pn=xsearch('<span class=.current.>\d+?</span><a class=.page larger. href="([^<]+?)">\d+?</a>',b);pn
		if pn:
			pages=xsearch('<a class="last" href="[^<]+page/(\d+?)/"',b)
			title=color['trangtiep']+'Page next: %d/%s[/COLOR]'%(page+1,pages)
			addir_info(title,pn,ico,'',mode,page+1,'tvhay_page',True)
	
	if query=='tvhay.org':
		body=get_home_page('tvhay.html','http://tvhay.org/phim-moi/')
		title=color['search']+"Search tr??n tvhay.org[/COLOR]"
		addir_info(title,'tvhay.org',ico,'',mode,1,'search',True)
		
		for i in ['PHIM M???I','PHIM XEM NHI???U','TH??? LO???I','QU???C GIA','PHIM B???','PHIM L???']:
			addir_info(namecolor(i,c),i,ico,'',mode,1,'menu',True)
		
		add_sep_item('--------------PHIM M???I C???P NH???T-------------');page=1;tvhay_page(body)
		
		if get_home_page('tvhay.html','http://tvhay.org/phim-moi/',True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif query=="INP":
		query=make_mySearch('',url,'','','','Input')
		if query:return tvhay(name,url,img,mode,page,query)
		else:return 'no'
	elif url=="tvhay.org":tvhay_page('http://tvhay.org/search/%s'%urllib.quote_plus(query))

	elif query=='menu':
		if url=='PHIM M???I':tvhay_page('http://tvhay.org/phim-moi/')
		elif url=='PHIM XEM NHI???U':
			body=get_home_page('tvhay.html','http://tvhay.org/phim-moi/')
			S=xsearch('(id="topview".+?class="block">)',body,1,re.DOTALL)
			for s in re.findall('(<ul.+?/ul>)',S,re.DOTALL):
				label=xsearch('class="tab (\w+)',s)
				add_sep_item('--------------%s-------------'%label)
				for i in re.findall('(<li>.+?</li>)',s):
					href=xsearch('href="(.+?)"',i)
					title=xsearch('title="(.+?)"',i)
					label=xsearch('<div class="views">(.+?)</div>',i)
					if label:title=title+' - [COLOR blue]%s[/COLOR]'%label
					addir_info(namecolor(title,c),href,ico,'',mode,1,'episode',True)
		elif url in ('TH??? LO???I','QU???C GIA'):
			body=get_home_page('tvhay.html','http://tvhay.org/phim-moi/')
			b='.h??? .o???i' if url=='TH??? LO???I' else 'Qu???c gia'
			s=xsearch('(<a>%s</a>.+?</ul>)'%b,body,1,re.DOTALL)
			for href,title in re.findall('href="(.+?)">(.+?)</a>',s):
				addir_info(namecolor(title,c),href,ico,'',mode,1,'tvhay_page',True)
		elif url=='PHIM B???':tvhay_page("http://tvhay.org/phim-bo/")
		elif url=='PHIM L???':tvhay_page("http://tvhay.org/phim-le/")
					
	elif query=='episode':
		b=make_request(url)
		s=make_request(xsearch('href="([^<]+?)" class="btn-watch"',b))
		S=xsearch('(class="serverlist".+?</ul></div></div>)',s)
		label=' '.join(xsearch('<title>(.+?)</title>',b).replace('|','-').replace('Phim','').split())
		if re.search('.huy???t .inh',label):label='[COLOR green]TM [/COLOR]- '+label
		elif re.search('.???ng .i???ng',label):label='[COLOR blue]LT [/COLOR]- '+label
		elif re.search(' Sub ',label):label='[COLOR blue]Sub [/COLOR]- '+label
		servers=re.findall('<div class="label">(.+?)</div>',S)
		for s in re.findall('(class="server".+?</ul>)',S):
			if len(servers)>1:add_sep_item('--------------%s-------------'%xsearch('<div class="label">(.+?)</div>',s))
			for title,href in re.findall('<a title="(.+?)" data-episode-id=".+?" href="(.+?)">',s):
				addir_info(title+' - '+label,href,img,'',mode,1,'play')
	
	elif query=='tvhay_page':tvhay_page(url)
	elif query=='play':#http://ndkchannel.com/ndkmusic.html http://nhacdj.vn/
		if 'http://tvhay.org/xem-phim' not in url:url=xsearch('href="([^<]+?)" class="btn-watch"',make_request(url))
		b=make_request(url)
		from resources.lib.servers import tvhay
		link=xsearch('link:"(.+?)"',tvhay(xsearch("(\w{1000,},\w+,\w+,\w+)",b.replace("'",''))).string)
		j=make_post('http://tvhay.org/tvhayplayer/plugins/gkpluginsphp.php',data={'link':link},resp='j')
		#print json.dumps(j,indent=2)
		L=[(s.get('link'),resolu(s.get('label'))) for s in j.get('link',list())];link=''
		L=sorted(L, key=lambda k: int(k[1]),reverse=True if myaddon.getSetting('resolut')=='Max' else False)
		for href,label in L:
			link=dl(href)
			if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','tvhay.org') 
	
def television(name,url,img,fanart,mode,page,query,text):
	fptlive_ico=icon['fptplay'];c='orange'
	hplus_ico='http://static.hplus.com.vn/themes/front/images/logo_hplus.png';hplus='http://hplus.com.vn/'
	xemtvhd_ico='http://xemtvhd.com/logo/xemtvhd.png';xemtvhd='http://www.xemtvhd.com/'
	vtvgo_ico=os.path.join(iconpath,'vtvgo.png')
	hd['x-requested-with']='XMLHttpRequest';hd['referer']=''
	def fixs(string):return ' '.join(re.sub('&.+;',xsearch('&(\w).+;',s),s) for s in string.split())
	
	if query=='Home':
		#data=urllib2.base64.b64decode('ZW1haWw9eHNoYXJlQHRoYW5odGhhaS5uZXQmcGFzc3dkPXhzaGFyZWFkZG9u')
		#o=make_post('http://hplus.com.vn/user/login/',data=data)
		#hd['Cookie']=o.cookiestring
		addir_info(namecolor('Truy???n h??nh FPTplay.net',c),'',fptlive_ico,'',mode,1,'fptlive',True)
		addir_info(namecolor('Truy???n h??nh VTVGo.vn','blue'),'Home',vtvgo_ico,'',56,1,'Home',True)
		b=make_request('http://hplus.com.vn/ti-vi-truc-tuyen/kenh-htv',headers=hd,resp='o')
		if b:cookie=b.cookiestring;b=b.body
		else:cookie=''
		s=xsearch('("dropdown-menu sub-left".+?</ul>)',b,1,re.DOTALL).replace('\n','')
		for href,title in re.findall('<a href="(.+?)">(.+?)</a>',s):
			title=namecolor(fixs(title.strip()),c)+' - [COLOR green](H+)[/COLOR]'
			addir_info(title,href,hplus_ico,'',mode,1,'hplus',True)
		
		#addir_info(namecolor('Truy???n h??nh XemTVHD.com',c),xemtvhd,xemtvhd_ico,'',mode,1,'xemtvhd',True)
		add_sep_item('---------------K??NH HTV tr??n Hplus (H+)----------------')
		for s in re.findall('(class="panel".+?</div>\s*</div>)',b,re.DOTALL):
			href=hplus+xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('<a href="[^<]+?">(.+?)</a>',s)
			addir_info(namecolor(fixs(title.strip()),c),href,img,'',mode,1,'hplus_play',text=cookie)
	
	elif query=='xemtvhd':
		body=get_home_page('xemtvhd.html',url)
		b=make_request(url)
		
		for s in re.findall("(<h2 class='title'>.+?</ul>)",b,re.DOTALL):
			label=xsearch("<h2 class='title'>(.+?)</h2>",s)
			add_sep_item('----------------%s----------------'%label)
			for i in re.findall('(<a.+?/a>)',s,re.DOTALL):
				href=xsearch("href='(.+?)'",i)
				#title=xsearch("alt='(.+?)'",i).replace('K??nh ','').replace(' Online','')
				img=xsearch("src='(.+?)'",i)
				title=xsearch('/([^/]+?).png',img).upper()
				addir_info(namecolor(title,c),href,img,'',mode,1,'xemtvhd_play')
		
		if checkupdate('xemtvhd.html',240,xsharefolder):
			response=make_request(url,hd,resp='o')
			if response:
				endxbmc();makerequest(joinpath(xsharefolder,'xemtvhd.html'),response.body,'w')
				xbmc.executebuiltin("Container.Refresh")
		
	elif query=='xemtvhd_play':
		b=make_request(url)#;f=open(r'd:\xoa.html','w');f.write(b);f.close()
		s=xsearch('(<div id="server">.+?</div>)',b,1,re.DOTALL);print s
		link=''
		for href in re.findall('href="(.+?)"',s):
			while href and not link:
				print 'href0: '+href
				b=make_request(href)
				href=[h for h in re.findall('src=[\'|\"](http.+?)[\'|\"]',b) if '.php' in h]
				if href:href=href[0];print 'href1: '+href
				else:link=xsearch('"(http.+?m3u8)"',b);print 'link:'+link,href
				if link and make_request(link):break
			print 'link..............'+link
		if link:xbmcsetResolvedUrl(link)#+'|Referer='+href)
		else:mess('Get channel link fail!') 

	elif query=='xemtvhd_play':
		name=namecolor(name).replace('HD','').lower()
		b=make_request('http://vps.tivi12h.net/vtv-go.php?id='+name)
		link=xsearch("file\": '(.+?)'",b)
		if link:xbmcsetResolvedUrl(link)
		else:mess('Get channel link fail!') 
		
	elif query=='hplus':
		b=make_request(url,headers=hd,resp='o')
		if b:cookie=b.cookiestring;b=b.body
		else:cookie=''
		for s in re.findall('(class="panel".+?</div>\s*</div>)',b,re.DOTALL):
			href=hplus+xsearch('href="(.+?)"',s)
			img=xsearch('src="(.+?)"',s)
			title=xsearch('<a href="[^<]+?">(.+?)</a>',s)
			addir_info(namecolor(fixs(title.strip()),c),href,img,'',mode,1,'hplus_play',text=cookie)
	
	elif query=='fptlive':
		from resources.lib.servers import fptPlay;fpt=fptPlay()
		for title,href,img in fpt.liveChannals():
			if 'sep' in href:add_sep_item('%s -----------------------------------------'%title)
			else:addir_info(namecolor(title,c),os.path.basename(href),img,'',mode,1,'fptlive_play')
	
	elif query=='fptlive_play':
		from resources.lib.servers import fptPlay;fpt=fptPlay()
		link=fpt.liveLink(url)
		if link:xbmcsetResolvedUrl(link)
		else:mess('Get channel link fail!') 
	
	elif query=='hplus_play':
		hd['Cookie']=text;hd['referer']=url
		b=make_request(url,headers=hd)
		link=xsearch('id="link-live" type="hidden" value="(.+?)"',b)
		data={'url':link,'type':'1'}
		link=post('http://hplus.com.vn/content/getlinkvideo/',data=data,headers=hd).body
		print data,link
		xbmcsetResolvedUrl(link)

def addir_info(name,url,img,fanart='',mode=0,page=1,query='',isFolder=False,text='',info={},art={},menu={}):
	def xquote(href):return urllib.quote_plus(href)
	def get_mode(url,name,mode,isfolder=True):
		if 'fshare.vn/' in url:
			id=xsearch('(\w{10,20})',url)
			if '/file/' in url:
				url='https://www.fshare.vn/file/%s'%id.upper()
				name='%sFshare[/COLOR] %s'%(color['fshare'],name);mode=3;isfolder=False
			else:
				url='https://www.fshare.vn/folder/%s'%id.upper()
				name='%sFshare %s[/COLOR]'%(color['fshare'],name);mode=90
		elif 'tenlua.vn/' in url:
			id=xsearch('(\w{10,20})',url)
			if 'folder/' in url or '#download' in url:
				url='https://tenlua.vn/fm/folder/%s'%id
				name='%sTenlua %s[/COLOR]'%(color['tenlua'],name);mode=95
			else:
				url='https://tenlua.vn/download/%s'%id
				name='%sTenlua[/COLOR] %s'%(color['tenlua'],name);mode=3;isfolder=False
		elif '4share.vn/d/' in url:name='%s4share %s[/COLOR]'%(color['4share'],name);mode=38
		elif '4share.vn/f/' in url:name='%s4share[/COLOR] %s'%(color['4share'],name);mode=3;isfolder=False
		elif 'subscene.com/' in url:name='%ssubscene[/COLOR] %s'%(color['subscene'],name);mode=94
		elif 'vaphim.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=1
		#elif 'vaphim.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=25
		elif 'phimfshare.com/' in url:name='%s%s[/COLOR]'%(color['vaphim'],name);mode=6
		elif 'hdvietnam.com' in url:name='%sHDVN[/COLOR] %s'%(color['hdvietnam'],name);mode=8
		elif 'taiphimhd.com' in url:name='%sTPHD[/COLOR] %s'%(color['taiphimhd'],name);mode=53
		return u2s(name),url,mode,isfolder
	
	def get_menu(menu,url):
		lists=list()

		if menu.has_key('muctheodoi'):
			inf=menu.get('muctheodoi')
			if [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to M???c ??ang theo d??i',{'query':'muctheodoi_Add'}))
			elif [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Remove from M???c ??ang theo d??i',{'query':'muctheodoi_Remove'}))
		
		if menu.has_key('MyFavourites'):
			inf=menu.get('MyFavourites')
			if [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to MyFavourites',{'query':'Add','mode':98}))
			if [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Remove from MyFavourites',{'query':'Remove','mode':98}))
		if menu.has_key('MyFshare'):
			inf=menu.get('MyFshare')
			if [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to MyFshare',{'query':'Add','mode':11}))
				lists.append(('Add to MyFshare Favorite',{'query':'AddFavorite','mode':11}))
				lists.append(('Add item name to string search',{'query':'Add','mode':13}))
			if [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Rename in MyFshare',{'query':'Rename','mode':11}))
				lists.append(('Remove from MyFshare',{'query':'Remove','mode':11}))
				lists.append(('Remove from MyFshare Favorite',{'query':'RemoveFavorite','mode':11}))
		
		if menu.has_key('MySearch'):
			inf=menu.get('MySearch')
			lists.append(('Rename item',{'query':'Rename','mode':9}))
			lists.append(('Remove item',{'query':'Remove','mode':9}))
		if menu.has_key('tuphim'):#menu={'tuphim':{'action':'Add','server':['phimmoi.net']}}
			inf=menu.get('tuphim')
			if inf['action']=='Add':
				lists.append(('Add to T??? phim c???a t??i',{'query':'tuphim_Add'}))
			elif inf['action']=='Remove':
				lists.append(('Remove from T??? phim c???a t??i',{'query':'tuphim_Remove'}))
		
		if menu.has_key('MyPlaylist'):
			inf=menu.get('MyPlaylist')
			if inf['action']=='Search':#cs:artist, sag tac:composer, ten alb:album, loi:lyric
				lists.append(('T??m ki???m theo: T??n b??i h??t/Ca s??',{'query':'csn_Search_None'}))
				lists.append(('T??m ki???m theo: Ca s??',{'query':'csn_Search_artist'}))
				lists.append(('T??m ki???m theo: S??ng t??c',{'query':'csn_Search_composer'}))
				lists.append(('T??m ki???m theo: T??n Album',{'query':'csn_Search_album'}))
				lists.append(('T??m ki???m theo: L???i b??i h??t',{'query':'csn_Search_lyric'}))
			elif [s for s in inf['server'] if s in url] and inf['action']=='Add':
				lists.append(('Add to My Playlist',{'query':'playlist_Add'}))
			elif [s for s in inf['server'] if s in url] and inf['action']=='Remove':
				lists.append(('Remove from My Playlist',{'query':'playlist_Remove'}))
				lists.append(('Remove all from My Playlist',{'query':'playlist_RemoveAll'}))
		elif menu.has_key('bookmark'):
			inf=menu.get('bookmark')
			if inf['action']=='Add':
				lists.append(('Th??m v??o H???p phim',{'query':'add_bookmark'}))
			elif inf['action']=='Remove':
				lists.append(('X??a kh???i H???p phim',{'query':'remove_bookmark'}))
		elif menu.has_key('hdonline'):
			inf=menu.get('hdonline')
			if inf['action']=='Add':
				lists.append(('Th??m v??o M???c Y??u th??ch',{'query':'Add'}))
			elif inf['action']=='Remove':
				lists.append(('X??a kh???i M???c Y??u th??ch',{'query':'Remove'}))
		elif menu.has_key('xshare'):
			inf=menu.get('xshare')
			if inf['action']=='Add':
				lists.append(('Th??m v??o M???c Y??u th??ch',{'query':'Add'}))
			elif inf['action']=='Remove':
				lists.append(('X??a kh???i M???c Y??u th??ch',{'query':'Remove'}))
		elif menu.has_key('myFavourites'):
			inf=menu.get('myFavourites')
			if 'Add' in inf['action']:
				lists.append(('Add to My Favourites V2',{'query':inf['action'],'mode':100+mode}))
			elif 'Remove' in inf['action']:
				lists.append(('Remove from My Favourites V2',{'query':inf['action'],'mode':101}))
		
		if menu.has_key('servers_list'):
			inf=menu.get('servers_list')
			if 'Up' in inf['action']:
				lists.append(('MoveUp',{'url':url,'mode':88,'query':'Up'}))
			if 'Down' in inf['action']:
				lists.append(('MoveDown',{'url':url,'mode':88,'query':'Down'}))
		return lists
	
	def add_menu(url):
		menu={'muctheodoi':{'action':'Add','server':['hdvietnam.com']}}
		menu['MyFshare']={'action':'Add','server':['fshare.vn']}
		menu['MyFavourites']={'action':'Add','server':['fshare.vn','4share.vn','tenlua.vn','subscene.com']}
		return menu
		
	if '18+' in name and phim18=="false":return
	server_mode=['fshare.vn','4share.vn','tenlua.vn','subscene.com','vaphim.com','phimfshare.com','hdvietnam.com']
	if mode not in [2,13] and [s for s in server_mode if s in url]:name,url,mode,isFolder=get_mode(url,name,mode)
	if not fanart:fanart=joinpath(home,'fanart.jpg')
	if not info:info={"title":name}
	if not art:art={"fanart":fanart}
	item=xbmcgui.ListItem(label=name,iconImage=img,thumbnailImage=img)
	item.setInfo(type="Video",infoLabels=info);item.setArt(art)
	if not isFolder:item.setProperty('IsPlayable', 'true')
	li='%s?name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s&text=%s'
	li=li%(sys.argv[0],xquote(name),xquote(url),xquote(img),xquote(fanart),mode,page,xquote(query),xquote(text))
	if not menu:menu=add_menu(url)
	if not menu.get('myFavourites'):
		menu['myFavourites']={'action':'Add-'+query+'-'+('F' if isFolder else ''),'mode':100+mode}
	menu=get_menu(menu,url)
	
	if menu:
		cmd='RunPlugin(plugin://%s/?'%myaddon.getAddonInfo('id');items=list()
		for label,info in menu:#menu=[(label,{'query':x,...})]
			if info.has_key('name'):name=info.get('name')
			if info.has_key('url'):url=info.get('url')
			if info.has_key('img'):img=info.get('img')
			if info.has_key('fanart'):fanart=info.get('fanart')
			if info.has_key('mode'):mode=info.get('mode')
			if info.has_key('page'):page=info.get('page')
			query=info.get('query')
			command=cmd+'&name=%s&url=%s&img=%s&fanart=%s&mode=%d&page=%d&query=%s)'
			command=command%(xquote(name),xquote(url),xquote(img),xquote(fanart),mode,page,xquote(query))
			if 'Remove' in query:label='[COLOR red]%s[/COLOR]'%label
			else:'[COLOR lime]%s[/COLOR]'%label
			items.append(('[COLOR lime]%s[/COLOR]'%label,command))
		
		item.addContextMenuItems(items)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),li,item,isFolder)

def myFavourites(name,url,img,fanart,mode,page,query):
	from resources.lib.servers import fshare;lib_imported=True
	fs=fshare(myaddon.getSetting('usernamef'),myaddon.getSetting('passwordf'))
	if 'Add' in query:
		mess('myFavourites adding...','myFavourites')
		mode=mode-100;q=query.split('-');folder='1' if q[2] else '';query=q[1]
		s='%s,%s,%s,%s,%d,%d,%s,%s'%(name,url,img,fanart,mode,page,query,folder)
		if fs.myFavourites_add(s):mess('Add a item to MyFavourites success')
		else:mess('Add a item to MyFavourites Fail!')
		fs.logout()
	
	elif query=='xshare':
		mess('myFavourites loading...','myFavourites')
		for i in fs.myFavourites_loads():
			try:name,url,img,fanart,mode,page,query,folder,ids=i.split(',')
			except:continue
			folder=True if folder else False
			menu={'myFavourites':{'action':'Remove-%s'%ids}}
			addir_info(name,url,img,fanart,int(mode),int(page),query,folder,menu=menu)
	
	elif 'Remove' in query:
		mess('myFavourites removing...','myFavourites')
		if fs.myFavourites_remove(query.replace('Remove-','')):
			mess('Remove a item from MyFavourites success')
			xbmc.executebuiltin("Container.Refresh")
		else:mess('Remove a item from MyFavourites Fail!')
	fs.logout()

def imax(name,url,img,fanart,mode,page,query):
	def sc(s):
		if 'fshare' in s:n=color['fshare']+'FS[/COLOR] '
		elif '4share' in s:n=color['4share']+'4S[/COLOR] '
		elif 'tenlua' in s:n=color['tenlua']+'TL[/COLOR] '
		elif 'subscene' in s:n=color['subscene']+'SUB[/COLOR] '
		return n
		
	ico=os.path.join(iconpath,'imax.png');urlhome='http://i-max.vn/';c='chartreuse'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('https://lh3.googleusercontent.com/YQxZANBnYMTFC1DTlBlmQnfRWUUzL0j2LCbf1VQzLOfi53UH9HChEIrrAmdL6_u7KPSC=s170'),'wb')
		except:pass

	from resources.lib.servers import imax;imx=imax(c)
	if query=='imax.vn':
		b=xread('http://i-max.vn/index.php')#http://i-max.vn/forum/search.php?searchid=209844
		title=color['search']+"Search tr??n imax.vn[/COLOR]"
		addir_info(title,'imax.vn',ico,'',mode,1,'search',True)
		
		s=xsearch('(id="highqualitybox".+?/ul>)',b,1,re.S)
		href=urllib2.base64.b64encode(json.dumps(re.findall('<a href="(.+?)">(.+?)</a>',s)))
		addir_info(namecolor('High Quality Box',c),href,ico,'',mode,1,'menu',True)
		
		s=xsearch('(id="normalbox".+?/ul>)',b,1,re.S)
		href=urllib2.base64.b64encode(json.dumps(re.findall('<a href="(.+?)">(.+?)</a>',s)))
		addir_info(namecolor('Normal Quality Box',c),href,ico,'',mode,1,'menu',True)
		add_sep_item('[COLOR gold]B??i vi???t m???i[/COLOR]-----------------------------')

		for s in [i for i in re.findall('(<table.+?/table>)',b,re.S) if '"Show Printable Version"' in i]:
			title,href,img=imx.pageDetail(s)
			addir_info(namecolor(title,c),href,img,'',mode,1,'thread',True)
			
	elif query=='menu':
		for href,title in json.loads(urllib2.base64.b64decode(url)):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'category',True)
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="imax.vn" or query=="INP":#009789051051551375973:id317tow93q
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		
		href='https://www.googleapis.com/customsearch/v1element?key=AIzaSyCVAXiUzRYsML1Pv6RwSG1gunmMikTzQqY&'
		href+='rsz=filtered_cse&num=20&hl=en&prettyPrint=false&source=gcsc&gss=.com&'
		href+='cx=009789051051551375973:id317tow93q&googlehost=www.google.com&'
		href+='callback=google.search.Search.apiary19044&q=%s'%urllib.quote_plus('"%s"'%' '.join(query.split()))
		
		if 'Page next:' in name:href+='&start=%d'%((page-1)*20)
		else:page=1
		
		items=imx.search(href)
		for title,href,img,q in items:
			if 'Page next:' in title:addir_info(title,url,ico,'',mode,page+1,query,True)
			else:addir_info(namecolor(remove_tag(title),c),href,img,'',mode,1,q,True)

	elif query=='thread':
		for title,href,i in imx.thread(url):
			if not href:add_sep_item('[COLOR gold]%s[/COLOR]-----------------------------'%i);continue
			elif not title:title=namecolor(re.sub('\[.+\] ','',name));i=img
			else:title=namecolor(title,c)
			if 'http' not in href:href='http://i-max.vn/forum/'+href
			addir_info(title,correct_link(href),i,'',mode,1,query,True)
		
	elif query=='category':
		for title,href,i in imx.category(url):
			if not namecolor(title).strip() or not href:continue
			elif i=='pagenext' or not i:i=img;q=query
			else:q='thread';href='http://i-max.vn/forum/showthread.php?t=%s&page=1000'%xsearch('t=(\d+)',href)
			
			addir_info(namecolor(title,c),href,i,'',mode,1,q,True)
	
	elif query=='forum':
		for title,href,i in imx.category(url):
			if not namecolor(title).strip() or not href:continue
			elif i=='pagenext' or not i:i=img;q=query
			else:q='thread';href='http://i-max.vn/forum/showthread.php?t=%s&page=1000'%xsearch('t=(\d+)',href)
			
			addir_info(namecolor(title,c),href,i,'',mode,1,q,True)

def taiphimhd(name,url,img,fanart,mode,page,query):#RSS
	ico=os.path.join(iconpath,'taiphimhd.png');urlhome='http://taiphimhd.com/';c='blue'
	if not os.path.isfile(ico):
		try:makerequest(ico,get('http://taiphimhd.com/styles/default/xenforo/logo.og.png',headers=hd).body,'wb')
		except:pass

	from resources.lib.servers import taiphim;taiphim=taiphim(c)
	if query=='taiphimhd.com':
		title=color['search']+"Search tr??n taiphimhd.com[/COLOR]"
		addir_info(title,'taiphimhd.com',ico,'',mode,1,'search',True)
		
		addir_info(namecolor('M???c Th???o lu???n m???i nh???t',c),'http://taiphimhd.com/find-new/posts',ico,'',mode,1,'list',True)
		
		addir_info(namecolor('M???c Xem g?? h??m nay',c),urlhome+'forums/xem-gi-hom-nay.18/',ico,'',mode,1,'list',True)
		items=[('Xem g?? h??m nay',urlhome+'forums/xem-gi-hom-nay.18/'+'index.rss')]
		
		b=get_home_page('taiphimhd.html',urlhome)
		a=[i for i in re.findall('<h3 class="nodeTitle"><a href="(.+?)"[^<]+>(.+?)</a></h3>',b) if [j for j in ['Phim','Show','Ph??? ?????'] if j in i[1]] and 'Y??u c???u' not in i[1]]
		for href,title in a:
			addir_info(namecolor('M???c '+title,c),urlhome+href,ico,'',mode,1,'list',True)
			items.append((title,urlhome+href+'index.rss'))
		
		#add_sep_item('-----C??c m???c Th??ng tin nhanh RSS-----')
		#for title,href in items:
		#	addir_info(namecolor('RSS '+title,'gold'),href,ico,'',mode,1,'rss',True)
		
		if get_home_page('taiphimhd.html',urlhome,True):xbmc.executebuiltin("Container.Refresh")
		
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="taiphimhd.com" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		query=urllib.quote('+'.join(query.split()))
		for title,href,img in taiphim.search(query):
			print u2s(title),u2s(href),u2s(img)
			addir_info(namecolor(remove_tag(title),c),href,img,'',mode,1,'page',True)

	elif query=='list':
		for title,href,img in taiphim.getLists(url):
			if img=='ico' and page==1:img=ico;q='list'
			elif img=='ico':continue
			elif img=='next':
				img=ico;q=query;page=page+1
				name=re.sub('\[COLOR %s.+/COLOR\]'%color['trangtiep'],'',name)
				title=name+color['trangtiep']+' Trang tiep theo...trang %d/%s[/COLOR]'%(page,title)
			else:q='page'
			addir_info(title,href,ico if not img else img,'',mode,page,q,True)
	
	elif query=='page':
		for title,href,img in taiphim.getPage(url):
			if title=='name':add_sep_item('--%s--'%namecolor(name));continue
			elif title=='--C?? th??? b???n mu???n xem--':add_sep_item(title);continue
			elif not href:continue
			addir_info(title,href,img,'',mode,page,'page',True)
	
	elif query=='rss':
		b=taiphim.getRSS(url)

def imovies(name,url,img,fanart,mode,page,query):
	def dirs(s):
		title,href,img,fanart,dir=imv.getDetail(s) if type(s)==str else s
		if 'Page next' in title:addir_info(title,href,img,fanart,mode,page+1,'page',True)
		elif dir:addir_info(namecolor(title,c),href,img,fanart,mode,1,'eps',True)
		else:addir_info(title,href,img,fanart,mode,1,'play')
	
	ico=os.path.join(iconpath,'imovies.png');urlhome='http://imovies.vn/';c='orange'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('http://imovies.vn/Images/imovies_v3_1.png'),'wb')
		except:pass
	
	from resources.lib.servers import imovies;imv=imovies(c)
	if query=='imovies.vn':
		title=color['search']+"Search tr??n imovies.vn[/COLOR]"
		addir_info(title,'imovies.vn',ico,'',mode,1,'search',True)
		
		b=xread(urlhome)
		for href,title in re.findall('<a href="/([^/]+?)" title="([P|V].+?)">',b):
			if title=='Phim s???p chi???u':title='R???p phim'
			q='menu' if 'video' not in href else 'video'
			addir_info(namecolor(title,c),urlhome+href,ico,'',mode,1,q,True)
		
		S=[i for i in b.split('<div class="clearfix">') if '"top-mov"' in i or '<h3 class='in i]
		
		for s in S:
			i=xsearch('<h3.+?>([^<]+?)</',s,1,re.S).strip()
			if not i:add_sep_item('Top Movies ------------------------')
			elif 'Phim s???p chi???u' in i:continue
			else:add_sep_item('%s ------------------------'%i)
			if 'class="top-mov"' in s:
				for i in [j for j in s.split('<div class="it">') if '<div class="mo-info">' in j]:dirs(i)
		
			elif '"top-prev"' in s:
				for i in re.findall('(<div class="mvit".+?/div>)',s,re.S):dirs(i)
		
			elif 'class="mo-block"' in s or 'id="top-video"' in s:
				s=re.findall('(<li.+?/li>)',s,re.S)
				for i in [j for j in s if "name" in j or '"vm"' in j]:dirs(i)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="imovies.vn" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		
		add_sep_item('Speed search result ------------------------')
		for title,href,img in imv.search(urllib.quote_plus(query)):
			addir_info(title,href,img,'',mode,1,'eps',True)
		
		add_sep_item('All search result ------------------------')
		[dirs(s) for s in imv.getPage('http://imovies.vn/tim-kiem.html?key='+urllib.quote_plus(query))]

	elif query=='menu':
		b=xread(url)
		
		if 'R???p phim' in name:name='Phim s???p chi???u'
		s=xsearch('<a href="[^"]+?" title="%s"(.+?/ul>)'%namecolor(name),b,1,re.S)
		for href,title in imv.menu(s):
			if 'bang-xep-hang' in href:q='subpage'
			else:q='page'
			addir_info(namecolor(title,c),href,img,fanart,mode,1,q,True)
		
		for s in [i for i in b.split('<div class="clearfix">') if '<div class="mvit">'in i]:
			i=re.search('<a href="(.+?)" title="(.+?)"',s,)
			if i:
				href='http://imovies.vn'+i.group(1)
				title=i.group(2).replace('Xem p','P')
				if 'CategoryId' in href:q='page'
				else:q='subpage'
				addir_info(namecolor(title,'cyan'),href,img,fanart,mode,1,q,True)
				
			for i in re.findall('(<div class="mvit".+?/div>)',s,re.S):dirs(i)
	
	elif query=='page':[dirs(s) for s in imv.getPage(url)]
			
	elif query=='subpage':
		b=xread(url)
		if 'Ooops.???? C?? l???i x???y ra!' in b:mess(u'Ooops.???? C?? l???i x???y ra!','imovies.vn');return
		S=[i for i in b.split('<div class="mo-block">') if '"mo-list"' in i]
		for s in S:
			i=' '.join(xsearch('<h3.+?>([^<]+?)</',s,1,re.S).split())
			if i:add_sep_item('--------%s-------'%i)
			for s in [i for i in re.findall('(<li.+?/li>)',s,re.S) if '"name"' in i]:dirs(s)
	
	elif query=='eps':
		b=xread(url)
		for href,epi in re.findall('class=.part-movie. href="(.+?)" title=".+?">(.+?)</a>',b,re.S):
			if 'http' not in href:href='http://imovies.vn'+href
			epi=' '.join(epi.split())
			addir_info(epi+' '+namecolor(name),href,img,fanart,mode,1,'play')

	elif query=='video':
		for title,href,img in imv.video(url):
			if not href:add_sep_item('--------%s-------'%title)
			elif [i for i in ('/tivi-show/','/phim-ngan/','/album/','/liveshow/','/playlist/') if i in href]:
				addir_info(namecolor(title,c),href,img,'',mode,1,'epi-show',True)
			else:addir_info(title,href,img if img else ico,'',mode,1,'play')
	
	elif query=='epi-show':
		b=xread(url);items=[]
		for s in re.findall('(<li class="hor".+?/li>)',b,re.S):
			title,href,img=imv.videoDetail(s)
			addir_info(title,href,img if img else ico,'',mode,1,'play')
			
		
	elif query=='play':
		if ('/video/' in url or 'wobo.vn' in url):# and 'youtube.com' in img:
			b=xread(url)
			id=xsearch("loadVideoById\('(.+?)'\)",b)
			return play_youtube(id)
			
		link=''
		for href,label in imv.maxLink(url):
			link=dl(href)#;print href,label
			if link:break
		
		if link:xbmcsetResolvedUrl(link)
		else:
			b=xread(url)
			if 'Phim n??y ch??a ???????c ph??t h??nh tr??n IMovies' in b:
				mess(u'Phim n??y ch??a ???????c ph??t h??nh tr??n IMovies - s??? c???p nh???t trong th???i gian t???i','imovies.vn')
			else:mess('File invalid or deleted!','hdsieunhanh.com') 

def vietsubhd(name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'vietsubhd.png');urlhome='http://www.vietsubhd.com/';c='springgreen'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('https://lh3.googleusercontent.com/-dQlfS9xn87g/VZlzVLNxjZI/AAAAAAAADi4/V_HB-F9rGYg/s126/logo.png'),'wb')
		except:pass
	
	from resources.lib.servers import vietsubhd;vsh=vietsubhd(c)
	if query=='vietsubhd.com':
		title=color['search']+"Search tr??n vietsubhd.com[/COLOR]"
		addir_info(title,'vietsubhd.com',ico,'',mode,1,'search',True)
		
		b=xread(urlhome);ec=urllib2.base64.b64encode
		for s in [i for i in b.split('<li class="item">') if '<head>' not in i]:
			title=xsearch('>([^<]+?)</a>',s)
			if 'hot' in title:href='http://www.vietsubhd.com/phim-hot/';q='page';s=''
			elif 'Shows' in title:href='http://www.vietsubhd.com/phim-tvshows/';q='page';s=''
			elif 'Anime' in title:href='http://www.vietsubhd.com/phim-anime/';q='page';s=''
			else:href='';q='menu'
			if 'http' not in href:href=urlhome+href
			addir_info(namecolor(title,c),'',ico,'',mode,1,q,True,text=ec(s))
			
		add_sep_item('------------PHIM HAY NH???T------------')
		s=xsearch('(<div class="block-body slider">.+?<div class="block-foot">)',b,1,re.S)
		for s in re.findall('(<div class="inner".+?/div>)',s):
			title,href,img=vsh.detail(s);addir_info(title,href,img,'',mode,1,'eps',True)
	
		add_sep_item('------------PHIM L??? M???I------------')
		s=xread('http://www.vietsubhd.com/ajaxload',data='loadfilm=1&idTab=%23phimlemoi')
		for s in re.findall('(<li.+?/li>)',s):
			title,href,img=vsh.detail(s);addir_info(title,href,img,'',mode,1,'eps',True)
	
		add_sep_item('------------PHIM B??? M???I------------')
		s=xread('http://www.vietsubhd.com/ajaxload',data='loadfilm=1&idTab=%23phimbomoi')
		for s in re.findall('(<li.+?/li>)',s):
			title,href,img=vsh.detail(s);addir_info(title,href,img,'',mode,1,'eps',True)
	
		add_sep_item('------------PHIM B??? FULL------------')
		s=xread('http://www.vietsubhd.com/ajaxload',data='loadfilm=1&idTab=%23phimbofull')
		for s in re.findall('(<li.+?/li>)',s):
			title,href,img=vsh.detail(s);addir_info(title,href,img,'',mode,1,'eps',True)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="vietsubhd.com" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		
		for title,href,img in vsh.page('http://www.vietsubhd.com/tim-kiem/%s/'%urllib.quote_plus(query)):
			if 'Page next:' in title:title=title.replace('page',str(page+1));img=ico;q=query
			else:q='eps'
			addir_info(title,href,img,'',mode,page+1,q,True)

	elif query=='menu':
		b=urllib2.base64.b64decode(text)
		#if 'Th??? lo???i' in name:
		for href,title in re.findall('<a href="(.+?)" title="(.+?)"',b):
			if 'http' not in href:href=urlhome+href
			addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
			
	elif query=='page':
		if not url and 'Phim hot' in name:url='http://www.vietsubhd.com/phim-hot/'
		elif not url and 'TV Shows' in name:url='http://www.vietsubhd.com/phim-tvshows/'
		elif not url and 'Anime Vietsub' in name:url='http://www.vietsubhd.com/phim-anime/'
		
		for title,href,img in vsh.page(url):
			if 'Page next:' in title:title=title.replace('page',str(page+1));img=ico;q=query;dir=True;p=page+1
			elif '/phim-sap-chieu/' in url or '/xem-video/' in href:q='youtube';dir=False;p=0
			else:q='eps';dir=True;p=0
			addir_info(title,href,img,'',mode,p,q,dir)
		
	elif query=='youtube':
		if 'youtube.com' not in url:b=xread(url);yt=xsearch('"([^"]+youtube.com[^"]+)"',b)
		else:yt=url
		if yt:return play_youtube(xsearch('([\w|-]{10,20})',yt))
	
	elif query=='eps':
		if 'xem-phim.html' not in url:url+='xem-phim.html'
		for title,id in vsh.eps(url):
			if 'B???n Trailer' in title:q='youtube'
			else:q='play'
			addir_info(title+' '+namecolor(name),'id=%s'%id,img,'',mode,1,q)
			
		
	elif query=='play':
		link=''
		if 'xem-phim.html' not in url and 'id=' not in url:url+='xem-phim.html'
		for href,label in vsh.maxLink(url):
			link=dl(href)
			if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','vietsubhd.com') 

def mphim (name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'mphim.png');urlhome='http://mphim.net/';c='deepskyblue'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('https://www.baokim.vn/promote/phimhd-baokim/logo-phimhd.png'),'wb')
		except:pass
	
	from resources.lib.servers import mphim;mph=mphim(c)
	if query=='mphim.net':
		title=color['search']+"Search tr??n mphim.net[/COLOR]"
		addir_info(title,'mphim.net',ico,'',mode,1,'search',True)
		
		b=xread('http://mphim.net/phim/abc.html')
		s=xsearch('(<div id="menu".+?/div>)',b,1,re.S);ec=urllib2.base64.b64encode
		for href,title in re.findall('<li.?><h2><a href="(.+?)">(.+?)</a></h2>',s):
			href=href.replace('#','')
			if not href:
				i=xsearch('(%s.+?/ul>)'%title,s,1,re.S)
				j=[('http://mphim.net'+k[0],k[1]) for k in re.findall('<a href="(.+?)"[^<]*?>([^<]+?)</a>',i)]
				href=ec(str(j));q='menu'
			elif 'http' not in href:href='http://mphim.net'+href;q='page'
			addir_info(namecolor(title,c),href,ico,'',mode,1,q,True)
	
	elif query=="search":make_mySearch('',url,'','',mode,'get')
	elif url=="mphim.net" or query=="INP":
		if query=="INP":
			query=make_mySearch('',url,'','','','Input')
			if not query:return 'No'
		if 'Page next:' not in name:page=1
		print 'http://mphim.net/tim-kiem/%s.html'%'-'.join(query.split())
		for title,href,img,dir in mph.page('http://mphim.net/tim-kiem/%s.html'%'-'.join(query.split())):
			if 'Page next:' in title:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
			elif dir:addir_info(namecolor(title,c),href,img,'',mode,1,'eps',True)
			else:addir_info(title,href,img,'',mode,1,'play')
	
	elif query=='menu':
		for href,title in eval(urllib2.base64.b64decode(url)):
			addir_info(namecolor(title,c),href,ico,'',mode,1,'page',True)
	
	elif query=='page':
		for title,href,img,dir in mph.page(url):
			if 'Page next:' in title:addir_info(title.replace('page',str(page+1)),href,ico,'',mode,page+1,query,True)
			elif dir:addir_info(namecolor(title,c),href,img,'',mode,1,'eps',True)
			else:addir_info(title,href,img,'',mode,1,'play')
	
	elif query=='eps':
		l=mph.eps(url)
		if not l:addir_info(namecolor(name),url,img,'',mode,1,'play')
		else:l=[addir_info(title,href,img,'',mode,1,'play') for title,href in l]
	
	elif query=='play':
		for href,label in mph.maxLink(url):
			link=dl(href)
			if link:break
		if link:xbmcsetResolvedUrl(link)
		else:mess('File invalid or deleted!','mphim.net') 

def vtvgo (name,url,img,fanart,mode,page,query):
	ico=os.path.join(iconpath,'vtvgo.png');urlhome='http://vtvgo.vn/';c='green'
	if not os.path.isfile(ico):
		try:makerequest(ico,xread('http://vtvgo.vn/public/images/logo.png'),'wb')
		except:pass
	
	from resources.lib.servers import vtvgovn;vtv=vtvgovn(c)
	if query=='Home':
		title=color['search']+"Search tr??n vtvgo.vn[/COLOR]"
		addir_info(title,'vtvgo.vn',ico,'',mode,1,'search',True)
		
		menu=[("http://vtvgo.vn/tin-tuc.html","Tin t???c t???ng h???p","cat01"),
			("http://vtvgo.vn/kho-video.html","Gameshows","cat02"),
			("http://vtvgo.vn/an-tuong-vtv.html","VTV Awards 2016","cat03")]
		
		for href,title,cat in menu:addir_info(namecolor('[B]%s[/B]'%title,c),href,ico,'',mode,1,cat,True)
		add_sep_item('VTVgo Live TV--------------------------------------')
		[addir_info(namecolor('[B]%s[/B]'%i[0],c),i[1],i[2],'',mode,1,'live') for i in vtv.liveList()]
		
	elif query=='cat01':#Tin t???c t???ng h???p
		for title in re.findall('<h2>(.+?)</h2>',xread(url)):
			addir_info(namecolor(title,c),'',ico,'',mode,1,'cat1',True)
	
	elif query=='cat1':
		if 'M???i Nh???t' in name:url='http://vtvgo.vn/get-data-news?keyword=new&page=%d'
		elif 'N??ng Nh???t' in name:url='http://vtvgo.vn/get-data-hot-news?keyword=hot&page=%d'
		elif 'Th???i S???' in name:url='http://vtvgo.vn/get-data-news?keyword=thoi+su&page=%d'
		elif 'Kinh T???' in name:url='http://vtvgo.vn/get-data-news?keyword=kinh+te&page=%d'
		elif 'Th??? Thao' in name:url='http://vtvgo.vn/get-data-news?keyword=the+thao&page=%d'
		elif 'Gi???i Tr??' in name:url='http://vtvgo.vn/get-data-news?keyword=giai+tri&page=%d'
		elif 'Th??? Gi???i' in name:url='http://vtvgo.vn/get-data-news?keyword=the+gioi&page=%d'
		for title,href,img in vtv.news(url,page):addir_info(title,href,img,img,mode,1,'play')
		
	elif query=='cat02':#Gameshows
		for title,href,img in vtv.cat02(url):
			if 'sep' in href:add_sep_item('%s --------------------------------------'%title)
			else:addir_info(title,href,img,img,mode,1,'play')
	
	elif query=='cat03':
		for title,href,img in vtv.cat03(url):
			if 'sep' in href:add_sep_item('%s --------------------------------------'%title)
			else:addir_info(title,href,img,img,mode,1,'play')
	
	elif query=='cat04':
		addir_info(namecolor('[B]VTV3 - [COLOR orange]FPT[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://118.69.252.4/tv2/vtv3HD/index.m3u8',ico,'',mode,1,'cat41')
		addir_info(namecolor('[B]VTV6 - [COLOR orange]FPT[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://118.69.252.4/tv2/vtv6HD/index.m3u8',ico,'',mode,1,'cat41')
		add_sep_item('-----------------------------------------------')
		
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 640x360',c),'1_ks4iwsda-01',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 854x480',c),'1_ks4iwsda-02',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1024x576',c),'1_ks4iwsda-03',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV3 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1280x720',c),'1_ks4iwsda-04',ico,'',mode,1,'golive')
		add_sep_item('-----------------------------------------------')
		
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 640x360',c),'1_rhex2pfs-01',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 854x480',c),'1_rhex2pfs-02',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1024x576',c),'1_rhex2pfs-03',ico,'',mode,1,'golive')
		addir_info(namecolor('[B]VTV6 - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1280x720',c),'1_rhex2pfs-04',ico,'',mode,1,'golive')
		add_sep_item('-----------------------------------------------')
		
		addir_info(namecolor('[B]VTV3 - [COLOR orange](D??? ph??ng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://live.tvmienphi.biz/stream-flix/vtv3hd.php','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv3-hd_145810226276.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV6 - [COLOR orange](D??? ph??ng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://live.tvmienphi.biz/stream-flix/vtv3hd.php','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv6-hd_14567302322.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV3 - [COLOR orange](D??? ph??ng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://embed.sohatv.vn?__c=vtv3','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv3-hd_145810226276.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV6 - [COLOR orange](D??? ph??ng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://embed.sohatv.vn?__c=vtv6','https://static.fptplay.net/static/img/share/channels/icon_channel_vtv6-hd_14567302322.jpg','',mode,1,'cat45')
		addir_info(namecolor('[B]VTV9 - [COLOR orange](D??? ph??ng)[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B]',c),'http://embed.sohatv.vn?__c=vtv9','http://vtv1.vcmedia.vn/web_images/vtv9-3.png','',mode,1,'cat45')
		add_sep_item('-----------------------------------------------')
		
		addir_info('[B][COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR] [COLOR red]N???i B???t[/COLOR][/B]','http://vtvgo.vn/euro2016/index.html',ico,'',mode,1,'cat42',True)
		addir_info('[B][COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR] [COLOR lime]Ph??t L???i[/COLOR][/B]','http://vtvgo.vn/euro2016/replay.html',ico,'',mode,1,'cat43',True)

	elif query=='cat45':
		if 'stream-flix' in url:
			link=xsearch('"file":\'(.+?)\'',xread(url))
			if 'VTV6' in name:link=link.replace('vtv3','vtv6')
		else:link=xsearch('playUrl.{3,5}"(.+?)"',xread(url))+'|Referer=http://vtv.vn/truyen-hinh-truc-tuyen.htm'
		xbmcsetResolvedUrl(link)

	elif query=='cat44':
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] Ch??? c?? Audio',c),'1_rhex2pfs',ico,'',mode,1,'golive_TYPE=AUDIO')
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 854x480',c),'1_rhex2pfs',ico,'',mode,1,'golive_854')
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1024x576',c),'1_rhex2pfs',ico,'',mode,1,'golive_1024')
		addir_info(namecolor('[B]VTV6 live - [COLOR red]VTVGo[/COLOR] [COLOR lime]Euro[/COLOR] [COLOR blue]2016[/COLOR][/B] 1280x720',c),'1_rhex2pfs',ico,'',mode,1,'golive_1280')
	
	elif query=='cat41':xbmcsetResolvedUrl(url)
	
	elif query=='golive':
		xbmcsetResolvedUrl(vtv.golive(url.split('-')[0],url.split('-')[1]))
		#xbmcsetResolvedUrl(joinpath(xsharefolder,'vtv.m3u8'))
	
	elif 'golive_' in query:
		url=vtv.golive(url)
		link=query.split('_')[1]
		base=urllib2.os.path.dirname(url)
		for i in xread(url).splitlines():
			if 'AUDIO' in link and link in i:link=xsearch('URI="(.+?)"',i);break
			elif link in i:link='OK';continue
			elif i and link=='OK':link=i;break
		link=base+'/'+link
		xbmcsetResolvedUrl(link)
	
	elif query=='cat42':
		b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LRzFuUzN5cUhKT28')
		url=urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b))
		[addir_info(i[0],i[1],i[2],'',mode,1,'playVOD') for i in vtv.vodList(url)]
	
	elif query=='cat43':
		b=xread('https://drive.google.com/folderview?id=0B5y3DO2sHt1LcGNoaC1QcUpldGs')
		url=urllib2.base64.b64decode(xsearch('<title>(.+?)</title>',b))
		[addir_info(i[0],i[1],i[2],'',mode,1,'playVOD') for i in vtv.vodList(url)]
		
	elif query=='playVOD':
		try:link=xbmcsetResolvedUrl(urllib2.urlopen(url).geturl()+'|Referer=http://vtvgo.vn/euro2016/live.html')
		except:mess('Get maxspeed link fail !','VTVgo.vn')
	
	elif query=='live':
		try:xbmcsetResolvedUrl(vtv.live(url))
		except:mess('Get maxspeed liveTV link fail !','VTVgo.vn')
	
	elif query=='play':
		try:xbmcsetResolvedUrl(vtv.vodLink(url))
		except:mess('Get maxspeed link fail !','VTVgo.vn')

try:#Container.SetViewMode(num) addir:name,link,img,fanart,mode,page,query,isFolder
	myfolder=s2u(myaddon.getSetting('thumuccucbo'))
	if not os.path.exists(myfolder):myfolder=joinpath(datapath,'myfolder')
except:myfolder=joinpath(datapath,'myfolder')
thumucrieng=''.join(s for s in myaddon.getSetting('thumucrieng').split()).upper()
if not thumucrieng or len(thumucrieng)<10:thumucrieng='RDA4FHXVE2UU'
thumucrieng='https://www.fshare.vn/folder/'+thumucrieng
subsfolder=joinpath(tempfolder,'subs');xsharefolder=os.path.join(tempfolder,'xshare')
params=get_params();mode=page=0;temp=[];url=name=fanart=img=date=query=action=end=text=''

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:img=urllib.unquote_plus(params["img"])
except:pass
try:fanart=urllib.unquote_plus(params["fanart"])
except:pass#xbmcsetResolvedUrl(link,sub)
try:mode=int(params["mode"])
except:pass#xbmc.executebuiltin("Container.Refresh")
try:page=int(params["page"])
except:pass#xbmc.executebuiltin("Container.Update")
try:query=urllib.unquote_plus(params["query"])
except:pass#urllib.unquote
try:text=urllib.unquote_plus(params["text"])
except:pass#urllib.unquote

#dialog = xbmcgui.Dialog()
#d = dialog.input('Enter secret code', type=xbmcgui.INPUT_ALPHANUM)
print '========================================================================'
print "Main--- Mode: "+str(mode),"Name: "+str(name),"URL: "+str(url),"Image: "+img,"query: "+query,"page: "+str(page)
print '========================================================================'


try:bakData=json.loads(xrw('sysmenu.dat'))
except:bakData={}
bakName=urllib2.hashlib.md5('%d%d%s%s%s'%(mode,page,query,name,url)).hexdigest()
myList=bakData.get(bakName)
if not myList:bakData[bakName]=[]

if myList:
	for name,url,img,fanart,mode,page,query,dir,menu in myList:
		addir_info(u2s(name),url,img,fanart,mode,page,query,dir,menu=menu)
elif not mode:#xbmc.executebuiltin("Dialog.Close(all, true)")
	init_file();open_category("MMN");endxbmc();xrw('sysmenu.dat',json.dumps({}))
	if myaddon.getSetting('checkdatabase')=='true' or os.path.isfile(joinpath(data_path,'checkdatabase.txt')):
		database_download()
	if myaddon.getSetting('auto_update')=='true' and checkupdate('xshare_auto_update.dat',5,datapath):
		makerequest(joinpath(datapath,"xshare_auto_update.dat"),'','w')
		xshare_auto_update();delete_files(tempfolder)		
elif mode==1:end=vaphim(name,url,img,fanart,mode,page,query)
elif mode==2:end=google_search(url,query,mode,page)
elif mode==3:end=resolve_url(url)
elif mode==4:vp_phimmoi()
elif mode==5:vp_xemnhieu()
elif mode==6:end=phimFshare(name,url,img,fanart,mode,page,query)
elif mode==7:end=fptplay(name,url,img,mode,page,query)
elif mode==8:end=hdvietnam(name,url,img,fanart,mode,page,query)
elif mode==9:make_mySearch(name,url,img,fanart,mode,query)
elif mode==10:open_category(query)
elif mode==11:make_myFshare(name,url,img,fanart,mode,query)
elif mode==12:make_mylist(name,url,img,fanart,mode,query)
elif mode==13:end=xshare_search(name,url,query,mode,page)
elif mode==15:end=id_2url(name,url,img,mode,page,query)
elif mode==16:end=play_maxspeed_link(url)
elif mode==17:end=megabox(name,url,img,fanart,mode,page,query)

elif mode==20:end=vp_update(auto=False)
elif mode==22:hdviet(name,url,img,mode,page,query)
elif mode==23:end=hayhaytv(name,url,img,fanart,mode,page,query)
elif mode==24:phimmoi(name,url,img,mode,page,query)
elif mode==25:search_get_page(name,url,img,fanart,mode,page,query)
elif mode==26:kenh88(name,url,img,mode,page,query)
elif mode==27:phimdata(name,url,img,mode,page,query)
elif mode==28:phim47(name,url,img,mode,page,query)
elif mode==29:phimsot(name,url,img,mode,page,query)
elif mode==30:hdonline(name,url,img,fanart,mode,page,query,bakName,bakData)
elif mode==31:end=ifile_update()
elif mode==32:phim3s(name,url,img,mode,page,query)
elif mode==33:kphim(name,url,img,mode,page,query)
elif mode==34:ifile_home(name,url,img,mode,page,query)
elif mode==35:phimnhanh(name,url,img,mode,page,query)
elif mode==36:bilutv(name,url,img,mode,page,query)
elif mode==37:anime47(name,url,img,mode,page,query)
elif mode==38:doc_Trang4share(url)#38
elif mode==39:phim14(name,url,img,mode,page,query)
elif mode==40:phimmedia(name,url,img,mode,page,query)
elif mode==41:tvhay(name,url,img,mode,page,query)
elif mode==42:nhacdj(name,url,img,fanart,mode,page,query)
elif mode==43:phimbathu(name,url,img,fanart,mode,page,query)
elif mode==44:hdsieunhanh(name,url,img,fanart,mode,page,query)
elif mode==45:chiasenhac(name,url,img,fanart,mode,page,query)
elif mode==46:nhaccuatui(name,url,img,fanart,mode,page,query)
elif mode==47:daklak47(name,url,img)
elif mode==48:imovies(name,url,img,fanart,mode,page,query)
elif mode==49:imax(name,url,img,fanart,mode,page,query)
elif mode==50:htvonline(name,url,img,fanart,mode,page,query)
elif mode==51:music(name,url,img,fanart,mode,page,query)
elif mode==52:myNAS(name,url,img,fanart,mode,page,query)
elif mode==53:taiphimhd(name,url,img,fanart,mode,page,query)
elif mode==54:vietsubhd(name,url,img,fanart,mode,page,query)
elif mode==55:mphim(name,url,img,fanart,mode,page,query)
elif mode==56:vtvgo(name,url,img,fanart,mode,page,query)
elif mode==88:servers_list(name,url,img,fanart,mode,page,query)
elif mode==89:television(name,url,img,fanart,mode,page,query,text)
elif mode==90:end=doc_TrangFshare(name,url,img,fanart,query)
elif mode==91:main_menu(url,page,mode,query)
elif mode==92:vp_list(name,url,img,mode,page,query)
elif mode==93:vp_chonloc()
elif mode==94:end=subscene(name,url,query)
elif mode==95:tenlua_getlink(url)
elif mode==96:end=doc_thumuccucbo(name,url,img,fanart,mode,query)
elif mode==97:doc_list_xml(url,name,page)
elif mode==98:make_favourites(name,url,img,fanart,mode,query)
elif mode==99:myaddon.openSettings();end='ok'
elif mode>100:myFavourites(name,url,img,fanart,mode,page,query)
if not end or end not in 'no-ok-fail':endxbmc()
#print json.dumps(a.json,indent=2,ensure_ascii=False)
