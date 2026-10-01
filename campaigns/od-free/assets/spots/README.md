# Drop the spot files here

The Outlook connector can read the email but cannot download video attachments,
so these seven files need to be added by hand. They are attached to Creed's
email to Dominic (Sep 30, "Re: OD Free on MCTV screens - stop by tomorrow",
Swayze CC'd). Save them with these exact names:

```
MCTV_OD-Free_MSDH_Spots-for-approval_2026-09-30.pdf
MCTV_OXF_ODFreeCommonAndDeadly_Paid_15s_v2.mp4
MCTV_OXF_ODFreeCommonAndDeadly_Paid_10s_v2.mp4
MCTV_OXF_ODFreeFentanylAnywhere_Paid_15s_v2.mp4
MCTV_OXF_ODFreePreventDeaths_Paid_10s_v2.mp4
MCTV_OXF_ODFreeRequestNaloxone_Paid_10s_v2.mp4
MCTV_OXF_ODFreeSaveALife_Paid_15s_v2.mp4
```

Two easy ways to add them:

1. On GitHub, open this folder and use **Add file → Upload files**.
2. Attach them in the Claude chat and ask Claude to put them here.

Then run `../../social/reels/build_reels.sh` to generate the vertical reels.
