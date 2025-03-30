# Turning Markdown into HTML Nodes

## First Steps

1. take markdown and _split_ into blocks
2. determine block type of each block
3. turn each **block** into an HTML node

## Considerations

### Helper Functions

- text to children
- heading level
- tag blocks

#### Let's Make a `Code` Block

```
def heading_level(text):
	match = re.match(r'^(#{1-6})\s', text)
	if match:
		return len(match.group(1))
	return 0
```

##### Now Let's Make a Quote Block

>This is a quote block.
>It should correctly be turned into a quote block.
>It should be able to handle **bold** and _italic_ within the quote.

###### Final Heading

- This will be an unordered list.
- Let's include an ![image](image_url)
- We'll include a bit of `code` as well.
- And, finally, a [link](link_url)

I almost forgot to add normal paragraph type blocks. Whoops.
This is a normal paragraph.

This is a second paragraph. It will contain **children** of _different_ types to `ensure` correct ![node](formation) and [node](assignment).