My gists :)

I ported them from gist.github.com so that I could easily mirror them in my private gitea instance.
I used two scripts to help me:

* Clone all my public gists as subtrees, so that their history could be merged into this repository's
* Rename the gists based on either the gist description or file name (for gists with a single file)

After that, the result was pretty much usable, and I only needed to merge/remove some of the repositories.


To use the script you will need pygithub:

```
pip install pygithub
```
