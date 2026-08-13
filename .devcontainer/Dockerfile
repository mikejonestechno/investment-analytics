FROM mcr.microsoft.com/devcontainers/anaconda:1.2.9-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
# COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/
# RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 \
#    && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; \
#    fi \
#    && rm -rf /tmp/conda-tmp

# [Optional] Uncomment to downgrade a different version of Python than the default
# RUN conda install -y python=3.6 \
#    && pip install --no-cache-dir pipx \
#    && pipx reinstall-all

# [Optional] Uncomment this section to install additional OS packages.
# Remove the base image's stale yarn apt source first - its signing key can no longer
# be verified (NO_PUBKEY 62D54FD4003F6525), which breaks apt-get update entirely.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends ruby-full build-essential \
    && gem install jekyll:4.4.1 bundler jekyll-seo-tag:2.8.0 jekyll-remote-theme:0.4.3 jekyll-redirect-from:0.16.0 jekyll-feed:0.17.0 \
    && rm -rf /var/lib/apt/lists/*