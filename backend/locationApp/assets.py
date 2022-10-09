from flask_assets import Bundle

bundles = {
  'general_style' : Bundle(
    'scss/style.scss',
    filters='libsass',
    output='gen/home.%(version)s.css'
  )
}