<svelte:head>
  <title>ADBTV</title>
</svelte:head>

<main>
  <TopAppBar variant="static" color="primary">
    <Row>
      <Section>
        <IconButton class="material-icons">menu</IconButton>
        <Title>AdBlock TV</Title>
      </Section>
      <Section align="end" toolbar>
        {#if !state.active}
          <IconButton class="material-icons" aria-label="Download" on:click={resume}>play_circle</IconButton>
        {:else}
          <IconButton class="material-icons" aria-label="Download" on:click={pause}>pause_circle</IconButton>
        {/if}
      </Section>
    </Row>
  </TopAppBar>
</main>

<script>
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import IconButton from '@smui/icon-button';
  
  let state = {
    active: true
  };

  function resume() {
    eel.setState({
      active: true
    })
  }

  function pause() {
    eel.setState({
      active: false
    })
  }

  function updateState(newState) {
    state = newState;
  }
  eel.expose(updateState);
</script>

<style>
  main {
    margin: -8px;
  }
</style>