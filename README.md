# HashCollider

This software try to find a new text file such that the hash of the initial hash is equal to the hash of the original file.
The new file is found by executing word substitution with a synonyms database defined by the user.


## Usage

First, you should define an hashfunction; to do this create a new file in the 'hashf' directory; the file should
include a function called 'evaluteHash(text)' that receive a plain text and returns its hash as string:

```python
import md5

def evaluteHash (text):
	return md5.new(text).hexdigest()
```

After that, create a text file that contains the base text:

```
Ciao %[mondo]%, questo e un base text di %[prova]%.
```

Every word that need to be replaced, should be inside '%[' ']%'.

Now define a synonyms file, that for each line contains the original word and synonyms of the original word.

```
mondo;terra;globo
prova;test
```

Now we have all we need, then start the software:

```bash
python hashcollider.py base.txt syn.txt 61e83bb5d399935e75df960badc594e3 md5_f
```

And wait! The software ends if:
- A forgery is found
- All combinations are done

If a forgery is found, the software writes a file 'result.txt'.


## Test case included

```bash
python hashcollider.py examples/base.txt examples/syn.txt 66dc6f md5_6dig
```
