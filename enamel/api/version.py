# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Microversion handling."""

import collections

# TODO(cdent): Get a real one, get it from config or other source of
# defaults.
SERVICE_TYPE = 'enamel'

# The Canonical Version List
VERSIONS = [
    '0.1',
]


def max_version_string():
    return VERSIONS[-1]


def min_version_string():
    return VERSIONS[0]


def parse_version_string(version_string):
    """Turn a version string into a Version

    :param version_string: A string of two numerals: X.Y
    :returns: a Version
    :raises: ValueError
    """
    if version_string == 'latest':
        version_string = max_version_string()
    try:
        # The combination of int and a limited split with the
        # named tuple means that this incantation will raise
        # ValueError or TypeError when the incoming data is
        # poorly formed but will, however, naturally adapt to
        # extraneous whitespace.
        return Version(*(int(value) for value
                         in version_string.split('.', 1)))
    except (ValueError, TypeError):
        raise ValueError('invalid version string: %s' % version_string)


class Version(collections.namedtuple('Version', 'major minor')):
    """A namedtuple containing major and minor values.

    Since it is a tuple is automatically comparable.
    """

    HEADER = 'OpenStack-%s-API-Version' % SERVICE_TYPE

    MIN_VERSION = None
    MAX_VERSION = None

    def __str__(self):
        return '%s.%s' % (self.major, self.minor)

    @property
    def max_version(self):
        if not self.MAX_VERSION:
            self.MAX_VERSION = parse_version_string(max_version_string())
        return self.MAX_VERSION

    @property
    def min_version(self):
        if not self.MIN_VERSION:
            self.MIN_VERSION = parse_version_string(min_version_string())
        return self.MIN_VERSION

    def in_window(self):
        return self.min_version <= self <= self.max_version


def extract_version(headers):
    version_string = headers.get(Version.HEADER.lower(),
                                 min_version_string())
    request_version = parse_version_string(version_string)
    # We need a version that is in VERSION and within MIX and MAX.
    # This gives us the option to administratively disable a
    # version if we really need to.
    if (str(request_version) in VERSIONS and request_version.in_window()):
        return request_version
    raise ValueError('Unacceptable version header: %s' % version_string)