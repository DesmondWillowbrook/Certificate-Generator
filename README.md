# Certificate Generator

- Originally made for use for New Delhi Gavels Club.

## An example interaction:
```
Enter recipient name: A Very Long Name
Enter date: 24th March 2022
1: Best Hopscotch Player Award
2: Most Creative Painting Award
Please enter certificate (number): 1
```

Output:

![Sample certificate](A_Very_Long_Name_Best_Hopscotch_Player_Award_On_24th_March_2022.png)

This is what the default template looks like:

![Defaullt Template](template.png)

You can change `template.png` to a custom certificate as well.

## What is this doing?

The program takes input for name, date, and certificate types, and writes them on an image created from `template.png`.

- Scales excessively long field names to fit predefined boxes.
- Auto-centers and aligns text fields.
- Generates multiple certificates from a single template.

## Creating Custom Bounding Boxes

Best way to determine coordinates is to go
in Paint and draw a box around all the text, then note the coordinates you start,
and the point where your cursor stops.

You can be very generous with the boxes.

For example, these are the default bounding boxes for the sample certificate.

![Image with bounding boxes for text](box_illustration.png)

You can mess with the fonts, font sizes, spacing and define custom bounding boxes in [main.py](main.py).

## Security

This program only generates a photo that looks like a certificate. This is very easily forgable and thus should not be used as a proper document.

To ensure security/non-fungibility, what you _can_ do is use [GnuPG](https://www.gnupg.org/) to cryptographically sign these documents to prove that they are valid.

For more, you can do is read the [documentation](https://www.gnupg.org/gph/en/manual/c14.html) and [ a convenient signing menthod here](https://www.gnupg.org/gph/en/manual/x135.html#AEN160).

You can also look at the [Kleopatra](https://www.openpgp.org/software/kleopatra/) or [gpg4win](https://www.gpg4win.org/) projects for a graphical interface to GPG.