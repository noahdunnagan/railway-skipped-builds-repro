FROM alpine:3.20

# MARKER is a Railway service variable. Railway passes service variables as
# --build-arg by default (disableEnvVarsAsBuildArgs=false), so this ARG is
# populated at BUILD time and BAKED into the image below.
ARG MARKER=unset
RUN echo "baked_marker=${MARKER}" > /marker.txt

# On boot we print BOTH:
#   - baked_marker : frozen into the image at build time (the bug surface)
#   - RUNTIME_MARKER: read fresh from the environment at start (always correct)
# If SKIPPED_BUILDS reuses another env's image, the two will DISAGREE.
CMD ["sh", "-c", "echo \"BOOT baked=$(cat /marker.txt) runtime=MARKER=${MARKER}\"; tail -f /dev/null"]
