class EntryPoints(object):
    def __init__(self):
        raw_entry_pts = [
            'C:/Users/tjh',
            'C:\D13',
            'C:\D13-Git',
            'C:\D13-Offline Websites',
            'C:\D13-Python Projects',
            'C:\D13-RawData',
            'C:\Freemind-To-Wiki-IO',
            'C:\mnt-HackRF Tutorials',
            'C:\TJ-Scanner',
            'C:\z_Archive'
        ]

        self.entry_pts = []
        for pt in raw_entry_pts:
            self.entry_pts.append(pt.replace('/', '\\'))

        self.black_list = [
            '.git',
            'My Music',
            'bin'
        ]


if __name__ == '__main__':
    ep = EntryPoints()
    print('Done')
