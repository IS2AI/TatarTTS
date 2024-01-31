FROM mambaorg/micromamba:latest

ARG NEW_MAMBA_USER=mambauser
ARG NEW_MAMBA_USER_ID
ARG NEW_MAMBA_USER_GID
USER root

RUN if grep -q '^ID=alpine$' /etc/os-release; then \
      # alpine does not have usermod/groupmod
      apk add --no-cache --virtual temp-packages shadow; \
    fi && \
    usermod "--login=${NEW_MAMBA_USER}" "--home=/home/${NEW_MAMBA_USER}" \
        --move-home "-u ${NEW_MAMBA_USER_ID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NEW_MAMBA_USER}" \
        "-g ${NEW_MAMBA_USER_GID}" "${MAMBA_USER}" && \
    if grep -q '^ID=alpine$' /etc/os-release; then \
      # remove the packages that were only needed for usermod/groupmod
      apk del temp-packages; \
    fi && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NEW_MAMBA_USER}" > "/etc/arg_mamba_user" && \
    :
ENV MAMBA_USER=$NEW_MAMBA_USER

USER $MAMBA_USER

# Install the rest projet dependencies
COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml env.yaml
RUN micromamba install --name base --verbose --yes --file env.yaml && \
    micromamba clean --all --yes


# ARG MAMBA_DOCKERFILE_ACTIVATE=1

#USER root
#USER $MAMBA_USER