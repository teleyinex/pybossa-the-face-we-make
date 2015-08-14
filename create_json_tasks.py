#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.
import click
import urllib
import urllib2
import json
import re
from optparse import OptionParser
import pbclient

import flickr

@click.command()
@click.option('--tags', default='Spike McCue', help='Album tags')
@click.option('--size', default='big', help='Photo size')
def get_flickr_photos(tags, size):
    """
    Gets public photos from Flickr feeds
    :arg string size: Size of the image from Flickr feed.
    :returns: A list of photos.
    :rtype: list
    """
    # Get the ID of the photos and load it in the output var
    print('Contacting Flickr for photos')
    url = "https://api.flickr.com/services/rest/"
    parameters = {
        'method': 'flickr.photos.search',
        'api_key': flickr.API_KEY,
        'user_id': '63147805@N03',
        'format':  'json',
        'tags': tags,
        'nojsoncallback': 1}

    query = url + "?" + urllib.urlencode(parameters)
    print query
    urlobj = urllib2.urlopen(query)
    data = urlobj.read()
    print data
    urlobj.close()
    # The returned JSON object by Flickr is not correctly escaped,
    # so we have to fix it see
    # http://goo.gl/A9VNo
    regex = re.compile(r'\\(?![/u"])')
    fixed = regex.sub(r"\\\\", data)
    output = json.loads(fixed)
    print('Data retrieved from Flickr')

    # For each photo ID create its direct URL according to its size:
    # big, medium, small (or thumbnail) + Flickr page hosting the photo
    photos = []
    url = 'https://api.flickr.com/services/rest'
    for photo in output['photos']['photo']:
        # Get photo info
        parameters = {
            'method': 'flickr.photos.getInfo',
            'api_key': flickr.API_KEY,
            'photo_id': photo['id'],
            'secret': photo['secret'],
            'format':  'json',
            'nojsoncallback': 1
        }
        query = url + "?" + urllib.urlencode(parameters)
        print query
        urlobj = urllib2.urlopen(query)
        data = urlobj.read()
        #print data
        urlobj.close()
        photo_data = json.loads(data)

        imgUrl_m = "http://farm%s.staticflickr.com/%s/%s_%s_m.jpg" % (photo['farm'], photo['server'], photo['id'], photo['secret'])
        imgUrl_b = "http://farm%s.staticflickr.com/%s/%s_%s_b.jpg" % (photo['farm'], photo['server'], photo['id'], photo['secret'])
        photos.append({'url_m':  imgUrl_m,
                       'url_b': imgUrl_b,
                       'photo_info': photo_data})

    task = dict(tags=tags,
                photos=photos)
    # Write the photos into a json file.
    filename = "photos_%s.json" % (tags.replace(' ', '_'))
    with open(filename, 'w') as f:
        f.write(json.dumps([task]))


if __name__ == '__main__':
    get_flickr_photos()
