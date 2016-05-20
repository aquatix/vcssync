# vcssync

Synchronise Git repos (and other vcs's in the future) at various locations, keeping them up-to-date (in sync) with each other.

Configure with a yaml file:

```yaml
# Start with a nickname. This needs to be unique, as it will be reflected in the local directory.
repo_a:
    # List the various locations, keys have to be unique within the project
    github: git@github.com:aquatix/vcssync.git
    live: aquatix@example.com:/opt/git/vcssync.git
mywebsite:
    github: git@github.com:aquatix/aquariusoft.git
    live: aquatix@example.com:/opt/git/aquariusoft.git
    local: /home/aquatix/projects/aquariusoft
    backup: ssh://backups.example.com/opt/backups/git/aquariusoft
```
