# Search_Engine
Developing a mini search-engine in python using reverse-indexed stemming and other SEOs implementations
## Part 1: The Reversed-Index
Create an inverted index for the corpus with data structures designed by you.
• Tokens: all alphanumeric sequences in the dataset.
• Stop words: do not use stopping while indexing, i.e. use all words, even
the frequently occurring ones.
• Stemming: use stemming for better textual matches. Suggestion: Porter
stemming, but it is up to you to choose.
• Important text: text in bold (b, strong), in headings (h1, h2, h3), and
in titles should be treated as more important than the in other places.
Verify which are the relevant HTML tags to select the important words.

Building the inverted index
Now that you have been provided the HTML files to index, you may build your
inverted index off of them. The inverted index is simply a map with the token
as a key and a list of its corresponding postings. A posting is the representation
of the token’s occurrence in a document. The posting typically (not limited to)
contains the following info (you are encouraged to think of other attributes that
you could add to the index):
• The document name/id the token was found in.
• Its tf-idf score for that document (for MS1, add only the term frequency).
Some tips:
• When designing your inverted index, you will think about the structure
of your posting first.
• You would normally begin by implementing the code to calculate/fetch
the elements which will constitute your posting.
• Modularize. Use scripts/classes that will perform a function or a set of
closely related functions. This helps in keeping track of your progress,
debugging, and also dividing work amongst teammates if you’re in a group.
• We recommend you use GitHub as a mechanism to work with your team
members on this project, but you are not required to do so.
