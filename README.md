# vcssync

Synchronise Git repos (and other vcs's in the future) at various locations, keeping them up-to-date (in sync) with each other.

Configure with a yaml file:

```yaml
# Start with a nickname. This needs to be unique, as it will be reflected in the local directory.
- repo_a
  # List the various locations
  - git@github.com:aquatix/vcssync.git
  - aquatix@example.com:/opt/git/vcssync.git
- mywebsite
  - git@github.com:aquatix/aquariusoft.git
  - aquatix@example.com:/opt/git/aquariusoft.git
  - /home/aquatix/projects/aquariusoft
```
