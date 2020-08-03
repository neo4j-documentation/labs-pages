// tag::config[]
CALL n10s.graphconfig.init({
  handleVocabUris: 'MAP', <1>
  handleMultival: 'ARRAY', <2>
  keepLangTag: true, <3>
  keepCustomDataTypes: true <4>
})
// end::config[]