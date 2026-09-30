# Banner Images

This folder contains promotional banner images for the QuickTym website.

## How to Add Banners

1. **Add your image file** to this folder:
   ```
   /public/banners/hero-banner.jpg
   /public/banners/category-outdoor.jpg
   /public/banners/promotion-summer.jpg
   ```

2. **Use in your components**:
   ```typescript
   <img src="/banners/hero-banner.jpg" alt="Hero Banner" />
   ```

## Recommended Banner Sizes

- **Hero Banner**: 1920x600px (width x height)
- **Category Banners**: 400x300px
- **Promotion Banners**: 600x400px

## Supported Formats

- `.jpg` / `.jpeg` - Best for photographs
- `.png` - Best for graphics with transparency
- `.webp` - Best for web (smaller file size)

## Example Banners to Create

1. **hero-banner.jpg** - Main homepage banner
   - Outdoor rental theme
   - "Rent Anything in 30 Minutes" message

2. **category-outdoor.jpg** - Outdoor category
   - Camping/nature theme
   - 400x300px

3. **category-tools.jpg** - Tools category
   - DIY/construction theme
   - 400x300px

4. **category-party.jpg** - Party category
   - Celebration/event theme
   - 400x300px

## Quick Start

For MVP, you can use free stock images from:
- [Unsplash](https://unsplash.com)
- [Pexels](https://pexels.com)
- [Pixabay](https://pixabay.com)

Search for:
- "camping tent" for outdoor
- "power drill" for tools
- "party celebration" for events

---

**Note**: All banner images will be automatically served from `/banners/` path in the frontend.
