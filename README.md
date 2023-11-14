<h1>Emotional Analysis of Russian Literature</h1>

— a vector space model based program for analyzing emotions in literary texts
inspired by <a href="https://github.com/matinho13/SentiArt">Sentiart.</a>

<p>We use a list of labels — nouns denoting the corresponding emotions, such as 
    <span style="font-family: cursive;">happiness</span> («schastye»), 
    <span style="font-family: cursive;">contentment</span> («udovolstvie»), 
    <span style="font-family: cursive;">surprise</span> («udivleniye»), 
    <span style="font-family: cursive;">anger</span> («zlost'»), 
    <span style="font-family: cursive;">sadness</span> («grust'»), 
    <span style="font-family: cursive;">fear</span> («strakh»), 
    <span style="font-family: cursive;">disgust</span> («otvrashcheniye»), and 
    <span style="font-family: cursive;">shame</span> («styd») to calculate the emotional values.
    For each word in the given text, the semantic proximity to each label is determined based on the cosine distance using the model  <span style="font-family: cursive;">fastText Skipgram</span> (trained on Russian National Corpus).</p>
<p></p> Words whose proximity to the label exceeded the threshold value considered semantic associates 
    => emotional lexis lists with weights.
    </p>

<p><strong>Possible applications:</strong><br>
<ul>
    <li>
        Analysis of the lexis associated with each of the emotions;
    </li>
    <li>
        Analysis of the distribution of emotional lexis across stories
    </li>
</ul>

<p><strong>Publications:</strong><br>

Moskvina, A., Kirina M. (2023). Where Is Happily Ever After? A Study of Emotions and Locations in Russian Short Stories of 1900-1930. In <em>Proceedings of Computational Linguistics – CompLing 2023</em> (in print).</p>

<p><strong>Acknowledgements:</strong><br>
The research is a part of project  <span style="font-family: cursive;">«Text as big data: the modeling of convergent processes in language and speech by computational methods»</span> within the Basic Research Program at HSE University in 2023.