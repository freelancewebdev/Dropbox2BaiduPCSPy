# -*- coding: utf-8 -*-
import ConfigParser
import dropbox
from baidupcs import PCS
import urllib2
import urllib
import json
import sys
import os
import time
import codecs

print ''
print 'Dropbox 2 Baidu PCS Py'
print ''  
print 'Copyright (C) 2014  Joe Molloy (info[at]hyper-typer.com)'
print 'This program comes with ABSOLUTELY NO WARRANTY.'
print 'This is free software, and you are welcome to redistribute it'
print ''
db_app_key = ''
db_app_secret = ''
db_access_token = ''
b_app_key = ''
b_app_secret = ''
b_access_token = ''
b_folder = ''
ignore_folders = []
secure_mode = False


localpath = os.path.dirname(os.path.abspath(__file__))
filecount = 0
filesize = 0
logfilepath = localpath + '/log.txt'
errcount = 0
dbclient = dropbox.client
dbpath = '/'
curdbpath = '/'
curbpath = ''
bpath = ''

tempdir = localpath + '/temp'

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def local_setup():
	global db_app_key, db_app_secret, db_ignore_folders, db_access_token, b_app_key, b_app_secret, b_folder, b_access_token, ignore_folders, secure_mode, curbpath, bpath
	print 'Preparing local system...'
	if not os.path.exists(tempdir):
		print 'Creating temporary folder...'
		try:
			os.makedirs(tempdir)
			print 'Local system ready!'
		except IOError:
			print 'Could not create temporary folder. Bye!'
			sys.exit()
	print 'Preparing log file...'
	if not os.path.exists(logfilepath):
		print 'Creating log file...'
		try:
			f = open(logfilepath,'w')
			f.write('Starting At: ' + time.strftime("%c"))
			f.close()
		except IOError:
			print 'Could not create log file. Bye!'
			sys.exit()
	else:
		print 'Initialising log file...'
		f = open(logfilepath,'w')
		f.write('Starting At: ' + time.strftime("%c"))
		f.close()
	print 'System setup complete.  Ready to start!'
	print 'Checking configuration data...'
	cfg = ConfigParser.ConfigParser()
	try:
		cfg.read('Dropbox2BaiduPCS_sample.cfg')
	except:
		print 'There was a problem reading the config file'
		print 'Please ensure you have renamed'
		print '\'Dropbox2BaiduPCS_sample.cfg\' to \'pymygreater.cfg\''
		print 'and added your own values as appropriate'
		sys.exit()
	try:
		db_app_key = cfg.getstring('dropbox','db-app-key')
	except:
		print 'No Dropbox application key set in config file'
		sys.exit()
	if not db_app_key:
		print 'No Dropbox application key set in config file'
		sys.exit();
	else:
		print 'db_app_key is ' + db_app_key
	try:
		db_app_secret = cfg.getstring('dropbox','db-app-secret')
	except:
		print 'No Dropbox application secret set in config file'
		sys.exit()		
	if not db_app_secret:
		print 'No Dropbox applicatiolication secret set in config file'
		sys.exit()
	try:
		b_app_key = cfg.getstring('baidu','b-app-key')
	except:
		print 'No Baidu application key set in config file'
		sys.exit()
	if not b_app_key:
		print 'No Baidu application key set in config file'
		sys.exit()
	try:
		b_app_secret = cfg.getstring('baidu','b-app-secret')
	except:
		print 'No Baidu application secret set in config file'
		sys.exit()
	if not b_app_secret:
		print 'No Baidu application secret set in config file'
		sys.exit()
	try:
		b_folder = cfg.getstring('baidu','b-folder')
	except:
		print 'No Baidu applicatio folder set in config file'
		sys.exit()
	if not b_folder:
		print 'No Baidu application folder set in config file'
		sys.exit()
	db_ignore_folders = cfg.getstring('dropbox','db-ignore-folders')
	if db_ignore_folders:
		ignore_folders = db_ignore_folders.split(',')
	else:
		ignore_folders = []
	try:
		secure_mode = cfg.getboolean('app','secure-mode')
	except:
		pass
	try:
		db_access_token = cfg.getstring('dropbox','db-access-token')
	except:
		pass
	try:
		b_access_token = cfg.getstring('baidu','b-access-token')
	except:
		pass
	curbpath = '/apps/' + b_folder + '/dropbox'
	bpath = '/apps/' + b_folder + '/dropbox'

def db_auth(db_app_key,db_app_secret):
	global db_access_token
	print 'Authenticating with Dropbox'
	print 'Checking for previously obtained Dropbox access token...'
	if db_access_token: 
		print 'Previously obtained Dropbox access token found!'
	else:
		flow = dropbox.client.DropboxOAuth2FlowNoRedirect(db_app_key, db_app_secret)
		authorize_url = flow.start()
		print '1. Go to: ' + authorize_url
		print '2. Click "Allow" (you might have to log in first)'
		print '3. Copy the authorization code.'

		code = raw_input("Enter the authorization code here: ").strip()
		db_access_token, user_id = flow.finish(code)
		cfg = ConfigParser.ConfigParser()
		cfg.set('dropbox','db_access_token',db_access_token)
		cfgfile = open('Dropbox2BaiduPCS_sample.cfg','w')
		cfg.write(cfgfile)
		cfgfile.close()
	dbclient = dropbox.client.DropboxClient(db_access_token)
	dbclientinfo = dbclient.account_info()
	print 'Dropbox Linked Account: ', dbclientinfo['display_name']
	print 'Dropbox Quota: ' + sizeof_fmt(dbclientinfo['quota_info']['quota'])
	print 'Dropbox Used: ' + sizeof_fmt(dbclientinfo['quota_info']['normal'])
	print 'Dropbox Ready!'
	return dbclient

def b_auth(b_app_key,b_app_secret):
	global b_access_token
	print 'Authenticating with Baidu'
	if not b_access_token
		code_url = 'https://openapi.baidu.com/oauth/2.0/device/code?'
		code_url += 'client_id=' + b_app_key
		code_url += '&response_type=device_code'
		code_url += '&scope=basic netdisk'
		response = urllib2.urlopen(code_url)
		data = json.load(response)
		reply = raw_input("Enter 'y' here when you have submitted the user code '" + data['user_code'] + "' at " + data['verification_url']).strip()
		if reply == 'y':
			code_url = 'https://openapi.baidu.com/oauth/2.0/token?'
			code_url += 'grant_type=device_token' 
			code_url += '&code=' + data['device_code']
			code_url += '&client_id=' + b_app_key
			code_url += '&client_secret=' + b_app_secret
			response1 = urllib2.urlopen(code_url)
			data1 = json.load(response1)
			if not ('error' in data1):
				b_access_token = data1['access_token']
				cfg = ConfigParser.ConfigParser()
				cfg.set('Baidu',b_access_token)
				cfgfile = open('Dropbox2BaiduPCS.cfg','w')
				config.write(cfgfile)
				cfgfile.close()
			else:
				reply = raw_input("Authentication failed.  Do you wish to try again? (y/n)").strip()
				if reply == 'y':
					b_auth(b_app_key,b_app_secret)
				else:
					print 'OK, bye!'
					sys.exit()

		else:
			reply = raw_input("Do you wish to try to authorise with Baidu again? (y/n)").strip()
			if reply == 'y':
				b_auth(b_app_key,b_app_secret)
			else:
				print 'OK, bye!'
				sys.exit()
	if(b_access_token != ''):
		pcs = PCS(b_access_token)
		qresponse = pcs.info()
		qdata = qresponse.json()
		print 'Baidu Quota: ' + sizeof_fmt(float(qdata["quota"]))
		print 'Baidu Used: ' + sizeof_fmt(float(qdata['used']))
		qdata = pcs.meta('/apps/mygreater/dropbox').json();
		if ('error_code' in qdata):
			print 'Creating Dropbox folder on Baidu...'
			qdata = pcs.mkdir(bpath)
			print 'Baidu Ready!'
		else:
			print 'Baidu Ready!'
		return pcs




def list_dirs(path):
	print 'Folders found in ' + path
	subdirs = [d['path'] for d in folder_metadata['contents'] if d['is_dir'] == True]
	for sd in subdirs:
		print sd

def list_files(path):
	global filecount, bpath, dbpath, curbpath, curdbpath
	for f in ignore_folders:
		if f in path:
			print 'Ignoring \'' + f + '\''
			return
	try:
		folder_metadata = dbclient.metadata(curdbpath)
	except:
		time.sleep(30)
		list_files(path)
	print 'Checking for files in \'' + path + '\' on Dropbox'
	subfiles = [d['path'] for d in folder_metadata['contents'] if d['is_dir'] == False]
	if(len(subfiles) > 0):
		for f in subfiles:
			filename = dbdownload(f)
			bupload(filename)
			filecount += 1
	else:
		print 'No files found.'
	print 'Checking for directories in \'' + path + '\' on Dropbox'
	subdirs = [d['path'] for d in folder_metadata['contents'] if d['is_dir'] == True]
	if(len(subdirs) > 0):
		for d in subdirs:
			print 'Looking at the \'' + d + '\' folder'
			curbpath = bpath + d
			curdbpath = d
			try:
				data = pcs.meta(curbpath).json();
			except:
				print 'Trying again in 30 seconds...'
				time.sleep(30)
				list_files(path)
			if ('error_code' in data):
				print 'Creating \'' + curbpath + '\' folder on Baidu...'
				try:
					data = pcs.mkdir(curbpath.encode('utf-8'))
					print '\'' + d + '\' folder created on Baidu...'
				except:
					print 'There was a problem creating the \'' + curbpath + '\' directory on Baidu'
					print 'Trying again in 30 seconds'
					time.sleep(30)
					list_files(path)
			try:
				list_files(curdbpath)
			except:
				print 'Trying again in 30 seconds...'
				time.sleep(30)
				list_files(path)
	else:
		print 'No directories found in \'' + path + '\' on Dropbox'
	if(curbpath != bpath):
		curdbpath = curdbpath.rsplit('/', 1)[0] 
		if(curdbpath == ''):
			curdbpath = '/'
		print 'Moving back up to ' + curdbpath + ' on Dropbox'
		curbpath = curbpath.rsplit('/', 1)[0]
		print 'Moving back up to ' + curbpath + ' on Baidu'



def dbdownload(filepath):
	global filesize
	filename = os.path.basename(filepath)
	try:
		f, metadata = dbclient.get_file_and_metadata(filepath)
		print 'Downloading ' + filename
	except:
		print filename + ' not found'
		return False
	try:
		out = open(tempdir + '/' + filename, 'wb')
		out.write(f.read())
		out.close()
		print filename + ' downloaded'
		filesize = filesize + os.path.getsize(tempdir + '/' + filename)
		return filename
	except IOError:
		print 'Problem saving ' + filename
		return False

def bupload(filename):
	global errcount
	if filename != False:
		print 'Preparing ' + filename + ' for upload...'
		try:
			fc = open(tempdir + '/' + filename, 'rb')
		except IOError:
			print 'Problem opening ' + filename
			return False
		try:
			response = pcs.upload((curbpath + '/' + filename).encode('utf-8'),fc, 'overwrite')
		except:
			if errcount < 10:
				print 'Ooops, issues encountered while uploading \'' + filename + '\' - retrying (try ' + str(errcount + 1) + ' of 10)...'
				errcount += 1
				time.sleep(30)
				response = pcs.upload((curbpath + '/' + filename).encode('utf-8'),fc, 'overwrite')
			else:
				print 'Ooops, there was a problem uploading ' + filename + ' to Baidu'
				f = codecs.open(logfilepath,'a', encoding='utf-8')
				f.write('Baidu Upload Failure: ' + curbpath + '/' + filename)
				f.close()
				return False
		if('error_code' in response.json()):
			print 'Ooops, there was a problem uploading ' + filename + ' to Baidu'
			f = codecs.open(logfilepath,'a', encoding='utf-8')
			f.write('Baidu Upload Failure: ' + curbpath + '/' + filename)
			f.close()
			return False
		else:
			print filename + ' uploaded to Baidu'
		fc.close()
		os.remove(tempdir + '/' + filename)


def do_cleanup():
	print 'Almost done, cleaning up...'
	for the_file in os.listdir(tempdir):
		file_path = os.path.join(tempdir, the_file)
    	try:
        	if os.path.isfile(file_path):
        		os.unlink(file_path)
    	except Exception, e:
        		print e
	print 'Temporary files deleted'
	if secure_mode:
		print 'Deleting access token files...'
		os.unlink(localpath + '/token')
		os.unlink(localpath + '/btoken')
		print 'Access token files deleted'

local_setup()
dbclient = db_auth(db_app_key,db_app_secret)
pcs = b_auth(b_app_key,b_app_secret)
list_files(dbpath)
do_cleanup()
print 'Closing log file...'
f = open(logfilepath,'a')
f.write('Finishing At: ' + time.strftime("%c"))
f.close()
print 'Logging done!'
if(filecount != 1):
	print str(filecount) + ' files uploaded (' + sizeof_fmt(filesize) + ')'
else:
	print str(filecount) + ' file uploaded (' + sizeof_fmt(filesize) + ')'