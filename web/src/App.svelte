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
  <section>
    <TabBar tabs={['Home', 'Ad-List']} let:tab bind:activeTab>
      <!-- Notice that the `tab` property is required! -->
      <Tab {tab} on:click={() => activeTab = tab}>
        <Label>{tab}</Label>
      </Tab>
    </TabBar>
    {#if activeTab === 'Home'}
      <List class="demo-list" dense>
        {#each state.blocks as block}
          <Item>
            <Graphic class="material-icons">stop_circle</Graphic>
            <Text>{block}</Text>
          </Item>
        {/each}
      </List>
    {/if}
    {#if activeTab === 'Ad-List'}
      <List class="demo-list" dense>
        {#each state.adlist as adname}
          <Item>
            <Graphic class="material-icons">stop_circle</Graphic>
            <Text>{adname}</Text>
          </Item>
        {/each}
      </List>
    {/if}
  </section>
</main>

<script>
  import TopAppBar, {Row, Section, Title} from '@smui/top-app-bar';
  import List, {Group, Item, Graphic, Meta, Separator, Subheader, Text, PrimaryText, SecondaryText} from '@smui/list';
  import Tab, {Icon, Label} from '@smui/tab';
  import TabBar from '@smui/tab-bar';
  import IconButton from '@smui/icon-button';
  
  let state = {
    active: true,
    blocks: [],
    adlist: []
  }
  let activeTab = "Home"

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

  if (typeof eel !== "undefined")
    eel.expose(updateState, "updateState");
</script>

<style>
  main {
    margin: -8px;
  }
</style>