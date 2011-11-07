import os, sys
import xbmc, xbmcgui
import simplejson as json

def delete_thumbnails(excl):
	sub_dirs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'Fanart']
	top_dir = xbmc.translatePath('special://thumbnails') + 'Video'
	for sdir in sub_dirs:
		dir = os.path.join(top_dir, sdir)
		files = os.listdir(dir)
		for f in files:
			if dp.iscanceled():
				return
			(name, ext) = os.path.splitext(f)
			if f in excl:
				continue
			if ext == '.dds':
				tmp = name + '.tbn'
				if tmp in excl:
					continue
			tmp = os.path.join(dir, f)
			if os.path.isfile(tmp):
				os.remove(tmp)

def get_movie_excl_list(excl):
	query = '{"jsonrpc": "2.0", "id": 1, '
	query += '"method": "VideoLibrary.GetMovies", '
	query += '"params": {"properties": ["fanart", "thumbnail"]}}'
	resp_json = xbmc.executeJSONRPC(query)
	resp_obj = json.loads(resp_json)
	if resp_obj['result'].has_key('limits'):
		if resp_obj['result']['limits']['total'] == 0:
			return
	else:
		return
	if resp_obj['result'].has_key('movies'):
		movies = resp_obj['result']['movies']
	else:
		return
	for m in movies:
		if m.has_key('fanart'):
			excl.add(os.path.basename(xbmc.translatePath(m['fanart'])))
		if m.has_key('thumbnail'):
			excl.add(os.path.basename(xbmc.translatePath(m['thumbnail'])))

def get_tvshows_excl_list(excl):
	query = '{"jsonrpc": "2.0", "id": 1, '
	query += '"method": "VideoLibrary.GetTVShows", '
	query += '"params": {"properties": ["fanart", "thumbnail"]}}'
	resp_json = xbmc.executeJSONRPC(query)
	resp_obj = json.loads(resp_json)
	if resp_obj['result'].has_key('limits'):
		if resp_obj['result']['limits']['total'] == 0:
			return
	else:
		return
	if resp_obj['result'].has_key('tvshows'):
		tvshows = resp_obj['result']['tvshows']
	else:
		return
	for t in tvshows:
		if t.has_key('fanart'):
			excl.add(os.path.basename(xbmc.translatePath(t['fanart'])))
		if t.has_key('thumbnail'):
			excl.add(os.path.basename(xbmc.translatePath(t['thumbnail'])))
		query = '{"jsonrpc": "2.0", "id": 1, '
		query += '"method": "VideoLibrary.GetSeasons", '
		query += '"params": {"tvshowid": %s, "properties": ["fanart", "thumbnail"]}}' % t['tvshowid']
		resp_json = xbmc.executeJSONRPC(query)
		resp_obj = json.loads(resp_json)
		if resp_obj['result'].has_key('limits'):
			if resp_obj['result']['limits']['total'] == 0:
				continue
		else:
			continue
		if resp_obj['result'].has_key('seasons'):
			seasons = resp_obj['result']['seasons']
		else:
			continue
		for s in seasons:
			if s.has_key('fanart'):
				excl.add(os.path.basename(xbmc.translatePath(s['fanart'])))
			if s.has_key('thumbnail'):
				excl.add(os.path.basename(xbmc.translatePath(s['thumbnail'])))
	query = '{"jsonrpc": "2.0", "id": 1, '
	query += '"method": "VideoLibrary.GetEpisodes", '
	query += '"params": {"properties": ["fanart", "thumbnail"]}}'
	resp_json = xbmc.executeJSONRPC(query)
	resp_obj = json.loads(resp_json)
	if resp_obj['result'].has_key('limits'):
		if resp_obj['result']['limits']['total'] == 0:
			return
	else:
		return
	if resp_obj['result'].has_key('episodes'):
		episodes = resp_obj['result']['episodes']
	else:
		return
	for e in episodes:
		if e.has_key('fanart'):
			excl.add(os.path.basename(xbmc.translatePath(e['fanart'])))
		if e.has_key('thumbnail'):
			excl.add(os.path.basename(xbmc.translatePath(e['thumbnail'])))

# get id for the current execution context.
cur_exec_ctx_id = int(sys.argv[1])

# Create dialogs
d = xbmcgui.Dialog()
dp = xbmcgui.DialogProgress()

# The exclude list.
excl_list = set()

dp.create('Thumbnail cleaner', 'Scanning...')
if dp.iscanceled():
	dp.close()
	del excl_list
	del dp
	del d
	sys.exit(0)
dp.update(50, 'Scanning movies...')
get_movie_excl_list(excl_list)
if dp.iscanceled():
	dp.close()
	del excl_list
	del dp
	del d
	sys.exit(0)
dp.update(100, 'Scanning TV shows...')
get_tvshows_excl_list(excl_list)
if dp.iscanceled():
	dp.close()
	del excl_list
	del dp
	del d
	sys.exit(0)
dp.close()
if d.yesno('Thumbnail cleaner', 'Delete unnecessary thumbnails'):
	dp.create('Thumbnail cleaner', 'Deleting thumbnails...')
	dp.update(25, 'Deleting thumbnails...')
	delete_thumbnails(excl_list)
	dp.close()
del d
del excl_list
del dp
