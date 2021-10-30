def recursive_add(src, store, dpth=0, key = ''):
    """ Recursively adds nested elements."""
    tabs = lambda n: ' ' * n * 4 # or 2 or 8 or...
    brace = lambda s, n: '%s%s%s' % ('['*n, s, ']'*n)

    if isinstance(src, dict):
        for key, value in src.iteritems():
            thisorg=Org(key,store=store)
            thisorg.reload_repos()
            thisorg.reload_members()
            print "Adding org: %s"%thisorg
            store.add_org(thisorg)
            print tabs(dpth) + brace(key, dpth)
            recursive_add(value, store, dpth + 1, key)
    elif isinstance(src, list):
        for litem in src:
            recursive_add(litem, store, dpth + 2)
    else:
        print "SRC is not dict nor list: '%s'" % src
        if key:
            print tabs(dpth) + '%s = %s' % (key, src)
        else:
            print tabs(dpth) + '- %s' % src
        thisorg=Org(src,store=store)
        thisorg.reload_repos()
        thisorg.reload_members()
        print "Adding org: %s"%thisorg
        store.add_org(thisorg)
