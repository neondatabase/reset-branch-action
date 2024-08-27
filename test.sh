echo "dsdsd-$(echo 5)"

cs () {
  neonctl cs branch \
  --project-id project_id \
  $(if [[ -n "$1" ]]; then echo "--pooled"; fi)
}

CS=$(cs)
CS_POOLED=$(cs true)